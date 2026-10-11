# Mathematical Foundations: Electromagnetics, Acoustics & CAD Differential Geometry

This document formalizes the mathematical principles of coupled multiphysics (Joule heating, MHD, acoustics) and the differential geometry underlying native CAD modeling (NURBS, B-Rep topology, conformal meshing).

---

## 1. Electromagnetics & Multiphysics Coupling

### 1.1 Quasi-Static Electric Conduction & Joule Heating
Under direct current (DC) or low-frequency conditions, Maxwell's equations reduce to electrostatics of current conduction:
$$\nabla \cdot \mathbf{J} = 0, \quad \mathbf{J} = \sigma_e \mathbf{E}, \quad \mathbf{E} = -\nabla V$$
Leading to the variable-conductivity elliptic Laplace/Poisson equation:
$$\nabla \cdot (\sigma_e \nabla V) = 0$$

Where:
- $V(\mathbf{x})$ is the electrical scalar potential $[\text{V}]$.
- $\sigma_e(T)$ is temperature-dependent electrical conductivity $[\text{S/m}]$.
- $\mathbf{J}$ is current density $[\text{A/m}^2]$.

#### Volumetric Joule Heat Source ($q_v$):
$$q_v = \mathbf{J} \cdot \mathbf{E} = \sigma_e \|\nabla V\|^2 = \frac{\|\mathbf{J}\|^2}{\sigma_e} \quad [\text{W/m}^3]$$
This source term $q_v$ directly couples as an internal heat source into the thermal diffusion solver:
$$\rho c_p \frac{\partial T}{\partial t} = \nabla \cdot (k \nabla T) + \sigma_e(T) \|\nabla V\|^2$$

### 1.2 Magnetohydrodynamics (MHD)
For an electrically conducting fluid (liquid metals, plasmas) moving at velocity $\mathbf{u}$ in magnetic flux density $\mathbf{B}$:
$$\mathbf{J} = \sigma_e (\mathbf{E} + \mathbf{u} \times \mathbf{B})$$
The resulting **Lorentz force** acting on the fluid element couples directly into the CFD momentum equation:
$$\mathbf{f}_{Lorentz} = \frac{1}{\rho} (\mathbf{J} \times \mathbf{B})$$

---

## 2. Acoustics & Wave Propagation

### 2.1 Acoustic Wave Equation (Time Domain)
For small-amplitude pressure perturbations $p'(\mathbf{x}, t)$ in a quiescent, inviscid, lossless fluid:
$$\frac{\partial^2 p'}{\partial t^2} - c_0^2 \nabla^2 p' = 0$$
Where $c_0 = \sqrt{\frac{K_s}{\rho_0}}$ is the speed of sound $[\text{m/s}]$ ($K_s$ adiabatic bulk modulus).

### 2.2 Helmholtz Equation (Frequency Domain)
Assuming harmonic acoustic time dependence $p'(\mathbf{x}, t) = \text{Re}\{ P(\mathbf{x}) e^{i \omega t} \}$:
$$\nabla^2 P + k_a^2 P = 0$$
Where acoustic wavenumber $k_a = \frac{\omega}{c_0} = \frac{2\pi f}{c_0}$.

---

## 3. CAD Differential Geometry & Exact B-Rep Mathematics

To model exact geometry without polygon approximations, the native CAD engine implements B-Rep (Boundary Representation) mathematics.

### 3.1 Non-Uniform Rational B-Splines (NURBS) Curves & Surfaces

#### 1. NURBS Curve:
$$\mathbf{C}(u) = \frac{\sum_{i=0}^n N_{i,p}(u) w_i \mathbf{P}_i}{\sum_{i=0}^n N_{i,p}(u) w_i}$$
Where:
- $\mathbf{P}_i \in \mathbb{R}^3$ are 3D control points.
- $w_i > 0$ are weights.
- $N_{i,p}(u)$ are $p$-th degree B-spline basis functions computed recursively via the Cox-de Boor algorithm over knot vector $U = \{u_0, u_1, \dots, u_m\}$.

#### 2. NURBS Surface:
$$\mathbf{S}(u, v) = \frac{\sum_{i=0}^n \sum_{j=0}^m N_{i,p}(u) N_{j,q}(v) w_{i,j} \mathbf{P}_{i,j}}{\sum_{i=0}^n \sum_{j=0}^m N_{i,p}(u) N_{j,q}(v) w_{i,j}}$$

Surface normal vector $\hat{\mathbf{n}}(u, v)$:
$$\hat{\mathbf{n}}(u, v) = \frac{\frac{\partial \mathbf{S}}{\partial u} \times \frac{\partial \mathbf{S}}{\partial v}}{\left\| \frac{\partial \mathbf{S}}{\partial u} \times \frac{\partial \mathbf{S}}{\partial v} \right\|}$$

Principal curvatures $\kappa_1, \kappa_2$ and Gaussian curvature $K = \kappa_1 \kappa_2$ determine exact surface curvature for aerodynamic and stress concentrations.

---

## 4. CAD-to-Simulation Conformal Meshing Mathematics

Converting continuous analytic B-Rep volumes into discrete simulation elements requires Delaunay triangulation and Voronoi diagram duals.

### 4.1 3D Delaunay Criterion
Given a set of points $\mathcal{P} \subset \mathbb{R}^3$, a tetrahedralization $\mathcal{T}$ is Delaunay if the circumsphere of every tetrahedron contains no other points of $\mathcal{P}$ in its interior:
$$\text{Circumsphere}(T) \cap \mathcal{P} = \emptyset \quad \forall T \in \mathcal{T}$$

### 4.2 Element Quality Metric (Aspect Ratio & Inradius)
To prevent numerical instability in FEA and CFD solvers, tetrahedral element quality $Q_T \in [0, 1]$ is computed as:
$$Q_T = \frac{3 \cdot r_{in}}{r_{out}} = \frac{3 \cdot (3V / A_{total})}{r_{out}}$$
Where:
- $r_{in}$ is inscribed sphere radius.
- $r_{out}$ is circumscribed sphere radius.
- $V$ is tetrahedron volume.
- $A_{total}$ is total surface area of the 4 faces.
- Regular equilateral tetrahedron has $Q_T = 1$; slivers approach $Q_T \to 0$.
The meshing pipeline strictly enforces $Q_T \ge 0.2$ across all computational domains.


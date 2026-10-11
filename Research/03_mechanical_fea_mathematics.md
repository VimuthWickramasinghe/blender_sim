# Mathematical Foundations: Mechanical Stress & Finite Element Analysis (FEA)

This document formalizes the continuum mechanics of solid deformation, linear elasticity, stress-strain tensors, failure criteria, and the Galerkin weak-form discretization implemented in the structural simulation engine.

---

## 1. Kinematics of Deformation & Strain Tensor

Let a deformable body occupy domain $\Omega_0 \subset \mathbb{R}^3$ in its undeformed reference configuration. The displacement field is defined as:
$$\mathbf{u}(\mathbf{X}, t) = \mathbf{x}(\mathbf{X}, t) - \mathbf{X}$$

### 1.1 Infinitesimal Strain Tensor
Under the assumption of small displacements and linear elasticity ($\|\nabla \mathbf{u}\| \ll 1$), the second-order symmetric infinitesimal strain tensor $\boldsymbol{\varepsilon}$ is:
$$\boldsymbol{\varepsilon} = \frac{1}{2} \left( \nabla \mathbf{u} + (\nabla \mathbf{u})^T \right)$$

In Cartesian components ($i, j \in \{x, y, z\}$):
$$\varepsilon_{ij} = \frac{1}{2} \left( \frac{\partial u_i}{\partial x_j} + \frac{\partial u_j}{\partial x_i} \right)$$

In engineering Voigt notation:
$$\boldsymbol{\varepsilon} = \begin{bmatrix} \varepsilon_{xx} & \varepsilon_{yy} & \varepsilon_{zz} & \gamma_{yz} & \gamma_{xz} & \gamma_{xy} \end{bmatrix}^T$$
Where engineering shear strain $\gamma_{ij} = 2 \varepsilon_{ij}$ for $i \ne j$.

---

## 2. Equilibrium & Cauchy Stress Tensor

The static equilibrium equations across volume $\Omega$ (ignoring inertia $\rho \ddot{\mathbf{u}} = \mathbf{0}$):
$$\nabla \cdot \boldsymbol{\sigma} + \mathbf{b} = \mathbf{0}$$
$$\boldsymbol{\sigma} = \boldsymbol{\sigma}^T \quad \text{(Angular momentum balance)}$$

Where:
- $\boldsymbol{\sigma}$ is the symmetric second-order Cauchy stress tensor $[\text{Pa}]$.
- $\mathbf{b}$ represents body forces per unit volume $[\text{N/m}^3]$ (e.g., gravity $\rho \mathbf{g}$).

### 2.1 Dynamic Equilibrium (Elastodynamics)
$$\nabla \cdot \boldsymbol{\sigma} + \mathbf{b} = \rho \frac{\partial^2 \mathbf{u}}{\partial t^2} + c \frac{\partial \mathbf{u}}{\partial t}$$
Where $c$ is viscous damping.

---

## 3. Constitutive Law: Generalized Hooke's Law

For linear elastic, isotropic materials, stress and strain are related by Lamé parameters $\lambda$ and $\mu$:
$$\boldsymbol{\sigma} = \lambda \text{tr}(\boldsymbol{\varepsilon}) \mathbf{I} + 2\mu \boldsymbol{\varepsilon}$$

Where Lamé parameters are defined from Young's modulus $E$ and Poisson's ratio $\nu$:
$$\mu = G = \frac{E}{2(1 + \nu)}, \quad \lambda = \frac{E \nu}{(1 + \nu)(1 - 2\nu)}$$

In matrix form (Voigt notation: $\boldsymbol{\sigma} = \mathbf{C} \boldsymbol{\varepsilon}$):
$$\begin{bmatrix} \sigma_{xx} \\ \sigma_{yy} \\ \sigma_{zz} \\ \sigma_{yz} \\ \sigma_{xz} \\ \sigma_{xy} \end{bmatrix} = \frac{E}{(1+\nu)(1-2\nu)} \begin{bmatrix} 
1-\nu & \nu & \nu & 0 & 0 & 0 \\
\nu & 1-\nu & \nu & 0 & 0 & 0 \\
\nu & \nu & 1-\nu & 0 & 0 & 0 \\
0 & 0 & 0 & \frac{1-2\nu}{2} & 0 & 0 \\
0 & 0 & 0 & 0 & \frac{1-2\nu}{2} & 0 \\
0 & 0 & 0 & 0 & 0 & \frac{1-2\nu}{2}
\end{bmatrix} \begin{bmatrix} \varepsilon_{xx} \\ \varepsilon_{yy} \\ \varepsilon_{zz} \\ \gamma_{yz} \\ \gamma_{xz} \\ \gamma_{xy} \end{bmatrix}$$

---

## 4. Yield Criteria & Scalar Invariants

### 4.1 Deviatoric Stress Tensor
$$\mathbf{s} = \boldsymbol{\sigma} - \frac{1}{3} \text{tr}(\boldsymbol{\sigma}) \mathbf{I}$$
Where hydrostatic mean stress $\sigma_m = \frac{1}{3} \text{tr}(\boldsymbol{\sigma}) = \frac{\sigma_{xx} + \sigma_{yy} + \sigma_{zz}}{3}$.

### 4.2 von Mises Equivalent Stress ($\sigma_v$)
Used widely for ductile materials (metals, polymers) to predict yield onset:
$$\sigma_v = \sqrt{\frac{3}{2} \mathbf{s} : \mathbf{s}} = \sqrt{\frac{1}{2} \left[ (\sigma_{xx}-\sigma_{yy})^2 + (\sigma_{yy}-\sigma_{zz})^2 + (\sigma_{zz}-\sigma_{xx})^2 + 6(\sigma_{xy}^2 + \sigma_{yz}^2 + \sigma_{xz}^2) \right]}$$

In terms of principal stresses $\sigma_1 \ge \sigma_2 \ge \sigma_3$:
$$\sigma_v = \frac{1}{\sqrt{2}} \sqrt{(\sigma_1 - \sigma_2)^2 + (\sigma_2 - \sigma_3)^2 + (\sigma_3 - \sigma_1)^2}$$

Yield occurs when $\sigma_v \ge \sigma_y$ (yield strength). Factor of Safety (FoS):
$$\text{FoS} = \frac{\sigma_y}{\sigma_v}$$

---

## 5. Finite Element Discretization (Galerkin Weak Form)

Multiply the equilibrium equation by test displacement vector $\mathbf{v} \in \mathcal{V}_0$ and integrate over domain $\Omega$:
$$\int_\Omega (\nabla \cdot \boldsymbol{\sigma}) \cdot \mathbf{v} \, d\Omega + \int_\Omega \mathbf{b} \cdot \mathbf{v} \, d\Omega = 0$$

Applying integration by parts and Gauss's divergence theorem:
$$\int_\Omega \boldsymbol{\sigma} : \boldsymbol{\varepsilon}(\mathbf{v}) \, d\Omega = \int_{\Gamma_t} \mathbf{t} \cdot \mathbf{v} \, d\Gamma + \int_\Omega \mathbf{b} \cdot \mathbf{v} \, d\Omega$$
Where $\mathbf{t} = \boldsymbol{\sigma} \hat{\mathbf{n}}$ is surface traction on boundary $\Gamma_t$.

### 5.1 Element Formulation
Discretizing with shape functions $\mathbf{N}_e(\mathbf{x})$:
$$\mathbf{u}(\mathbf{x}) \approx \mathbf{N}_e(\mathbf{x}) \mathbf{u}_e$$
$$\boldsymbol{\varepsilon} = \mathbf{B}_e \mathbf{u}_e, \quad \text{where } \mathbf{B}_e = \mathbf{L} \mathbf{N}_e$$

Element stiffness matrix $\mathbf{K}_e$:
$$\mathbf{K}_e = \int_{\Omega_e} \mathbf{B}_e^T \mathbf{C} \mathbf{B}_e \, d\Omega_e$$

Assembled global linear system:
$$\mathbf{K} \mathbf{u} = \mathbf{F}_{ext}$$
Solved using Sparse Cholesky factorization or Preconditioned Conjugate Gradients (PCG).


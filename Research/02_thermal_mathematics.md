# Mathematical Foundations: Thermal & Thermodynamic Simulation

This document outlines the continuum thermodynamics, heat transfer equations, and numerical discretization schemes implemented in the thermal simulation engine.

---

## 1. Governing Heat Equation

In a 3D isotropic continuum domain $\Omega \subset \mathbb{R}^3$, the conservation of thermal energy is governed by:

$$\rho c_p \frac{\partial T}{\partial t} = \nabla \cdot (k \nabla T) + q_v - \rho c_p (\mathbf{u} \cdot \nabla T)$$

Where:
- $T(\mathbf{x}, t)$ is the temperature field $[\text{K}]$.
- $\rho$ is the material density $[\text{kg/m}^3]$.
- $c_p$ is the specific heat capacity at constant pressure $[\text{J/(kg}\cdot\text{K)}]$.
- $k$ is the thermal conductivity tensor (scalar $k$ for isotropic media) $[\text{W/(m}\cdot\text{K)}]$.
- $q_v$ is volumetric heat generation rate (e.g., Joule heating, chemical reaction) $[\text{W/m}^3]$.
- $\mathbf{u}$ is fluid velocity field in convective heat transport $[\text{m/s}]$.

When thermal conductivity $k$ is homogeneous and spatial medium is stationary ($\mathbf{u} = \mathbf{0}$):
$$\frac{\partial T}{\partial t} = \alpha \nabla^2 T + \frac{q_v}{\rho c_p}$$
Where $\alpha = \frac{k}{\rho c_p}$ is the thermal diffusivity $[\text{m}^2/\text{s}]$.

---

## 2. Boundary Conditions

1. **Dirichlet Boundary Condition (Prescribed Temperature)**:
   $$T(\mathbf{x}, t) = T_w(\mathbf{x}, t) \quad \text{on } \Gamma_D$$
2. **Neumann Boundary Condition (Prescribed Heat Flux)**:
   $$-k \nabla T \cdot \hat{\mathbf{n}} = q''_w \quad \text{on } \Gamma_N$$
   *(Adiabatic / perfectly insulated surface: $q''_w = 0 \implies \frac{\partial T}{\partial n} = 0$)*.
3. **Robin / Cauchy Boundary Condition (Newton's Law of Cooling - Convective)**:
   $$-k \nabla T \cdot \hat{\mathbf{n}} = h_{conv} (T - T_\infty) \quad \text{on } \Gamma_R$$
   Where $h_{conv}$ is the convective heat transfer coefficient $[\text{W/(m}^2\cdot\text{K)}]$, $T_\infty$ is ambient fluid temperature.
4. **Thermal Radiation Boundary (Stefan-Boltzmann)**:
   $$q''_{rad} = \epsilon \sigma_{SB} (T^4 - T_{ambient}^4)$$
   Where $\sigma_{SB} \approx 5.670 \times 10^{-8} \, \text{W/(m}^2\cdot\text{K}^4)$, $\epsilon \in [0, 1]$ is surface emissivity.

---

## 3. Convective Coupling & Boussinesq Buoyancy

In natural convection, density variations drive fluid velocity through buoyancy body forces. Under the Boussinesq approximation (small temperature differences $\Delta T$):
$$\rho(T) \approx \rho_0 [1 - \beta (T - T_0)]$$
Where $\beta = -\frac{1}{\rho}\frac{\partial \rho}{\partial T}$ is the volumetric thermal expansion coefficient $[\text{K}^{-1}]$.

The buoyancy force per unit mass coupled back into the CFD momentum equation is:
$$\mathbf{f}_{buoyancy} = -\beta (T - T_0) \mathbf{g}$$

---

## 4. Numerical Discretization

### 4.1 Forward-Time Central-Space (FTCS - Explicit)
Discretized on a uniform grid with spacing $\Delta x, \Delta y, \Delta z$:
$$\nabla^2 T_{i,j,k}^n \approx \frac{T_{i+1,j,k}^n - 2T_{i,j,k}^n + T_{i-1,j,k}^n}{\Delta x^2} + \frac{T_{i,j+1,k}^n - 2T_{i,j,k}^n + T_{i,j-1,k}^n}{\Delta y^2} + \frac{T_{i,j,k+1}^n - 2T_{i,j,k}^n + T_{i,j,k-1}^n}{\Delta z^2}$$

Time integration update:
$$T_{i,j,k}^{n+1} = T_{i,j,k}^n + \Delta t \left[ \alpha \nabla^2 T_{i,j,k}^n + \frac{q_v}{\rho c_p} - (\mathbf{u} \cdot \nabla T)_{i,j,k}^n \right]$$

### 4.2 Stability Criterion (CFL Limit for Diffusion)
For explicit FTCS schemes, stability strictly requires:
$$\Delta t \le \frac{1}{2 \alpha \left( \frac{1}{\Delta x^2} + \frac{1}{\Delta y^2} + \frac{1}{\Delta z^2} \right)}$$
For uniform cubic grid ($\Delta x = \Delta y = \Delta z$ in 3D):
$$\text{Fourier Number } Fo = \frac{\alpha \Delta t}{\Delta x^2} \le \frac{1}{6}$$

### 4.3 Implicit Crank-Nicolson Scheme (Unconditionally Stable)
To bypass the strict $\Delta t \sim \Delta x^2$ time-step constraint for high-resolution grids:
$$\frac{T^{n+1} - T^n}{\Delta t} = \frac{\alpha}{2} \left[ \nabla^2 T^{n+1} + \nabla^2 T^n \right]$$
Rearranged into a sparse linear system $\mathbf{A} T^{n+1} = \mathbf{b}$, solved using Conjugate Gradient (CG) or BiCGSTAB via `scipy.sparse.linalg`.

---

## 5. Phase-Change Modeling (Enthalpy Method)

For melting and solidifying materials, latent heat $L$ $[\text{J/kg}]$ is modeled through total volumetric enthalpy $H(T)$:
$$H(T) = \int_{T_{ref}}^T \rho c_p \, dT + \rho L f_l(T)$$
Where liquid fraction $f_l(T) \in [0, 1]$ across the mushy zone $[T_{solidus}, T_{liquidus}]$:
$$f_l(T) = \begin{cases} 
0, & T < T_{solidus} \\
\frac{T - T_{solidus}}{T_{liquidus} - T_{solidus}}, & T_{solidus} \le T \le T_{liquidus} \\
1, & T > T_{liquidus}
\end{cases}$$


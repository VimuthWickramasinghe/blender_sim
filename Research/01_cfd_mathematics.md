# Mathematical Foundations: Computational Fluid Dynamics (CFD)

This document formalizes the governing continuum mechanics and mesoscopic kinetic theory implemented in the CFD solvers.

---

## 1. Governing Navier-Stokes Equations

For an incompressible, isothermal Newtonian fluid in continuous Euclidean space $\mathbb{R}^3$, the fluid motion is governed by the Navier-Stokes equations:

### 1.1 Continuity Equation (Mass Conservation)
$$\nabla \cdot \mathbf{u} = 0$$

Where:
- $\mathbf{u} = (u, v, w)^T$ is the velocity vector field $[\text{m/s}]$.

### 1.2 Momentum Conservation Equation
$$\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla)\mathbf{u} = -\frac{1}{\rho}\nabla p + \nu \nabla^2 \mathbf{u} + \mathbf{f}$$

Where:
- $\rho$ is the fluid density $[\text{kg/m}^3]$.
- $p$ is the static pressure field $[\text{Pa}]$.
- $\nu = \frac{\mu}{\rho}$ is the kinematic viscosity $[\text{m}^2/\text{s}]$.
- $\mathbf{f}$ represents external body forces per unit mass (e.g., gravity $\mathbf{g}$, buoyancy forces) $[\text{m/s}^2]$.

---

## 2. Lattice Boltzmann Method (LBM)

To maximize parallel computing throughput on GPUs via Taichi and NumPy, the primary fluid solver utilizes the mesoscopic Lattice Boltzmann Method based on the BGK (Bhatnagar-Gross-Krook) single relaxation time collision operator.

### 2.1 Discrete Lattice Boltzmann Equation
$$f_i(\mathbf{x} + \mathbf{c}_i \Delta t, t + \Delta t) - f_i(\mathbf{x}, t) = -\frac{1}{\tau} \left( f_i(\mathbf{x}, t) - f_i^{(eq)}(\mathbf{x}, t) \right) + F_i \Delta t$$

Where:
- $f_i(\mathbf{x}, t)$ is the particle distribution function along discrete lattice direction $i$.
- $\mathbf{c}_i$ is the discrete microscopic velocity vector for direction $i$.
- $\tau$ is the dimensionless relaxation time parameter, related directly to the kinematic viscosity $\nu$:
  $$\nu = c_s^2 \left( \tau - \frac{1}{2} \right) \Delta t$$
- $c_s = \frac{1}{\sqrt{3}} \frac{\Delta x}{\Delta t}$ is the lattice speed of sound.
- $f_i^{(eq)}$ is the local Maxwell-Boltzmann equilibrium distribution.

### 2.2 Discrete Velocity Models

#### D2Q9 Velocity Set (2D - 9 Directions):
Microscopic velocity vectors $\mathbf{c}_i \in \{0, \pm 1, \pm 1\}$:
$$\mathbf{c}_0 = (0, 0)$$
$$\mathbf{c}_{1..4} = (\pm 1, 0), (0, \pm 1)$$
$$\mathbf{c}_{5..8} = (\pm 1, \pm 1)$$

Lattice weights $w_i$:
$$w_0 = \frac{4}{9}, \quad w_{1..4} = \frac{1}{9}, \quad w_{5..8} = \frac{1}{36}$$

#### D3Q19 Velocity Set (3D - 19 Directions):
- Center: $w_0 = \frac{1}{3}$
- 6 faces: $w_{1..6} = \frac{1}{18}$
- 12 edges: $w_{7..18} = \frac{1}{36}$

### 2.3 Equilibrium Distribution Function
$$f_i^{(eq)}(\rho, \mathbf{u}) = w_i \rho \left[ 1 + \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2} + \frac{(\mathbf{c}_i \cdot \mathbf{u})^2}{2 c_s^4} - \frac{\mathbf{u} \cdot \mathbf{u}}{2 c_s^2} \right]$$

### 2.4 Macroscopic Quantities Reconstruction
$$\rho(\mathbf{x}, t) = \sum_{i} f_i(\mathbf{x}, t)$$
$$\mathbf{u}(\mathbf{x}, t) = \frac{1}{\rho(\mathbf{x}, t)} \sum_{i} \mathbf{c}_i f_i(\mathbf{x}, t)$$
$$p(\mathbf{x}, t) = c_s^2 \rho(\mathbf{x}, t)$$

---

## 3. Boundary Treatments

### 3.1 Half-Way Bounce-Back (No-Slip Wall)
For solid obstacles and walls located halfway between fluid node $\mathbf{x}_f$ and solid node $\mathbf{x}_s$:
$$f_{\bar{i}}(\mathbf{x}_f, t + \Delta t) = f_i^*(\mathbf{x}_f, t)$$
Where $\bar{i}$ is the inverse direction of $i$ ($\mathbf{c}_{\bar{i}} = -\mathbf{c}_i$), and $f_i^*$ is the post-collision distribution.

### 3.2 Zou-He Velocity Inlet / Pressure Outlet
For boundary nodes with prescribed macroscopic velocity $\mathbf{u}_w$:
$$f_i - f_i^{(eq)} = f_{\bar{i}} - f_{\bar{i}}^{(eq)}$$
Non-equilibrium bounce-back resolves the unknown incoming distributions while preserving conservation of mass and momentum.

---

## 4. Dimensionless Numbers & Stability Criteria

1. **Reynolds Number ($Re$)**:
   $$Re = \frac{U L}{\nu}$$
   Where $U$ is characteristic velocity, $L$ characteristic length.
2. **LBM Mach Number Condition ($Ma < 0.1$)**:
   To minimize compressibility errors in incompressible fluid approximations:
   $$Ma = \frac{U_{max}}{c_s} \ll 1$$
3. **Relaxation Stability Limit**:
   $$\tau > 0.5$$
   For numerical stability in standard BGK. As $\tau \to 0.5$, viscosity $\nu \to 0$; for high Reynolds turbulence, Smagorinsky subgrid-scale turbulence models or Multiple Relaxation Time (MRT) models are employed.

---

## 5. OpenFOAM Finite Volume Method (FVM) Formulation

While LBM operates on mesoscopic lattice velocity distributions, OpenFOAM solves the continuum macroscopic Navier-Stokes equations discretized over arbitrary polyhedral control volumes $V_P$:

### 5.1 Integral Form over Control Volume $V_P$
$$\int_{V_P} \frac{\partial (\rho \phi)}{\partial t} dV + \int_{\partial V_P} (\rho \mathbf{u} \phi) \cdot d\mathbf{S} = \int_{\partial V_P} (\Gamma_\phi \nabla \phi) \cdot d\mathbf{S} + \int_{V_P} S_\phi dV$$
Where $\phi \in \{1, u, v, w, T, k, \omega\}$ is the transported scalar or vector quantity, and $\Gamma_\phi$ is the diffusion coefficient.

Summing over face areas $\mathbf{S}_f = \hat{\mathbf{n}}_f A_f$:
$$\frac{\partial (\rho \phi)_P}{\partial t} V_P + \sum_f F_f \phi_f = \sum_f \Gamma_{\phi, f} (\nabla \phi)_f \cdot \mathbf{S}_f + S_\phi V_P$$
Where $F_f = \rho_f \mathbf{u}_f \cdot \mathbf{S}_f$ is the convective mass flux through face $f$.

### 5.2 Pressure-Velocity Coupling (SIMPLE & PISO)
Because the incompressible continuity equation ($\nabla \cdot \mathbf{u} = 0$) lacks a direct pressure time derivative, OpenFOAM couples velocity and pressure via Poisson pressure equations:

1. **Semi-Discretized Momentum Equation**:
   $$a_P \mathbf{u}_P = \mathbf{H}(\mathbf{u}) - \nabla p \implies \mathbf{u}_P = \frac{\mathbf{H}(\mathbf{u})}{a_P} - \frac{1}{a_P}\nabla p$$
   Where $\mathbf{H}(\mathbf{u}) = -\sum_{N} a_N \mathbf{u}_N + \mathbf{S}_{\mathbf{u}}$.
2. **Pressure Poisson Equation**:
   Substituting $\mathbf{u}$ into continuity $\nabla \cdot \mathbf{u} = 0$:
   $$\nabla \cdot \left( \frac{1}{a_P} \nabla p \right) = \nabla \cdot \left( \frac{\mathbf{H}(\mathbf{u})}{a_P} \right)$$
   - **SIMPLE (Semi-Implicit Method for Pressure-Linked Equations)**: Used in `simpleFoam` for steady-state flows.
   - **PISO / PIMPLE**: Used in `pimpleFoam` for transient, large-timestep simulations.

### 5.3 Turbulence Modeling: Two-Equation $k-\omega$ SST Model
The Shear Stress Transport ($k-\omega$ SST) formulation combines the accuracy of the Wilcox $k-\omega$ model near boundary-layer walls with the robust $k-\epsilon$ model in the free stream:

$$\frac{\partial (\rho k)}{\partial t} + \nabla \cdot (\rho \mathbf{u} k) = \nabla \cdot \left[ (\mu + \sigma_k \mu_t)\nabla k \right] + \tilde{P}_k - \beta^* \rho k \omega$$
$$\frac{\partial (\rho \omega)}{\partial t} + \nabla \cdot (\rho \mathbf{u} \omega) = \nabla \cdot \left[ (\mu + \sigma_\omega \mu_t)\nabla \omega \right] + \alpha \frac{\rho}{\mu_t}\tilde{P}_k - \beta \rho \omega^2 + 2(1 - F_1)\rho \sigma_{\omega 2}\frac{1}{\omega}\nabla k \cdot \nabla \omega$$

Turbulent kinematic eddy viscosity:
$$\nu_t = \frac{\mu_t}{\rho} = \frac{a_1 k}{\max(a_1 \omega, S F_2)}$$
Where $F_1, F_2$ are blending functions and $S = \sqrt{2 \mathbf{S}_{ij}\mathbf{S}_{ij}}$ is the strain rate magnitude.



# Mathematical Foundations: Particle Dynamics (SPH & DEM)

This document formalizes the Lagrangian mesh-free methods implemented for fluid particle dynamics (Smoothed Particle Hydrodynamics) and granular media (Discrete Element Method).

---

## 1. Smoothed Particle Hydrodynamics (SPH)

SPH discretizes continuous continuum fluid equations into discrete interacting interpolation points (particles) carrying mass $m_i$, density $\rho_i$, velocity $\mathbf{u}_i$, and pressure $p_i$.

### 1.1 Kernel Interpolation & Approximation
Any continuous field $A(\mathbf{x})$ and its spatial gradient $\nabla A(\mathbf{x})$ are interpolated over neighbor particles within smoothing kernel radius $h$:
$$A(\mathbf{x}_i) \approx \sum_{j} m_j \frac{A_j}{\rho_j} W(\mathbf{x}_i - \mathbf{x}_j, h)$$
$$\nabla A(\mathbf{x}_i) \approx \sum_{j} m_j \frac{A_j}{\rho_j} \nabla W(\mathbf{x}_i - \mathbf{x}_j, h)$$

### 1.2 Smoothing Kernels
1. **Cubic Spline Kernel ($M_4$)**:
   $$W(r, h) = \frac{\sigma}{h^d} \begin{cases} 
   1 - \frac{3}{2}q^2 + \frac{3}{4}q^3, & 0 \le q \le 1 \\
   \frac{1}{4}(2 - q)^3, & 1 < q \le 2 \\
   0, & q > 2 
   \end{cases}$$
   Where $q = \frac{r}{h}$, $r = \|\mathbf{x}_i - \mathbf{x}_j\|$, and $\sigma = \frac{1}{\pi}$ (in 2D) or $\frac{1}{\pi}$ (in 3D).
2. **Wendland $C^2$ Quintic Kernel** (prevents particle clustering and tensile instability):
   $$W(r, h) = \frac{21}{16\pi h^3} (1 - q/2)^4 (1 + 2q) \quad \text{for } q \le 2$$

### 1.3 Density Summation
$$\rho_i = \sum_{j} m_j W(\mathbf{x}_i - \mathbf{x}_j, h)$$

### 1.4 Equation of State: Tait's Weakly Compressible EOS
Relates local density fluctuations to pressure:
$$p_i = \frac{\rho_0 c_s^2}{\gamma} \left[ \left( \frac{\rho_i}{\rho_0} \right)^\gamma - 1 \right]$$
Where:
- $\rho_0$ is the reference rest fluid density (e.g., $1000 \, \text{kg/m}^3$ for water).
- $\gamma = 7$ for water.
- $c_s \ge 10 U_{max}$ is artificial speed of sound ensuring density variations $\frac{|\rho - \rho_0|}{\rho_0} \le 1\%$.

### 1.5 Momentum Equation (Symmetric Pressure Gradient)
$$\frac{d\mathbf{u}_i}{dt} = -\sum_{j} m_j \left( \frac{p_i}{\rho_i^2} + \frac{p_j}{\rho_j^2} \right) \nabla_i W_{ij} + \Pi_{ij} + \mathbf{g}$$

Where Monaghan's artificial viscosity tensor $\Pi_{ij}$:
$$\Pi_{ij} = \begin{cases} 
\frac{-\alpha_{visc} \bar{c}_{ij} \mu_{ij} + \beta_{visc} \mu_{ij}^2}{\bar{\rho}_{ij}}, & \mathbf{u}_{ij} \cdot \mathbf{x}_{ij} < 0 \\
0, & \mathbf{u}_{ij} \cdot \mathbf{x}_{ij} \ge 0 
\end{cases}$$
Where $\mu_{ij} = \frac{h (\mathbf{u}_{ij} \cdot \mathbf{x}_{ij})}{\|\mathbf{x}_{ij}\|^2 + 0.01 h^2}$, $\bar{c}_{ij} = \frac{c_i + c_j}{2}$, $\bar{\rho}_{ij} = \frac{\rho_i + \rho_j}{2}$.

---

## 2. Discrete Element Method (DEM) for Granular Media

Models individual macroscopic particles (spheres with radius $R_i, R_j$, mass $m_i, m_j$).

### 2.1 Contact Overlap & Kinematics
For two spherical particles with centers $\mathbf{x}_i, \mathbf{x}_j$:
$$\delta_n = (R_i + R_j) - \|\mathbf{x}_i - \mathbf{x}_j\|$$
Contact normal vector $\hat{\mathbf{n}} = \frac{\mathbf{x}_i - \mathbf{x}_j}{\|\mathbf{x}_i - \mathbf{x}_j\|}$. Contact occurs when $\delta_n > 0$.

### 2.2 Normal Contact Force (Hertzian Contact Theory)
$$F_n = \frac{4}{3} E^* \sqrt{R^*} \delta_n^{3/2} - \gamma_n \dot{\delta}_n$$

Where:
- Equivalent radius $R^* = \frac{R_i R_j}{R_i + R_j}$.
- Equivalent Young's modulus $\frac{1}{E^*} = \frac{1-\nu_i^2}{E_i} + \frac{1-\nu_j^2}{E_j}$.
- $\gamma_n$ is normal damping coefficient related to restitution coefficient $e_{rest}$.

### 2.3 Tangential Contact Force & Coulomb Friction
Mindlin-Deresiewicz contact model with Coulomb friction cutoff:
$$\mathbf{F}_t = -\min\left( k_t \boldsymbol{\delta}_t + \gamma_t \mathbf{v}_t, \mu_{fric} |F_n| \right) \hat{\mathbf{t}}$$
Where $\mu_{fric}$ is sliding friction coefficient, $\hat{\mathbf{t}}$ is tangential slip unit direction.

### 2.4 Particle Integration (Velocity Verlet)
$$\mathbf{x}_i(t + \Delta t) = \mathbf{x}_i(t) + \mathbf{v}_i(t)\Delta t + \frac{1}{2m_i}\mathbf{F}_i(t)\Delta t^2$$
$$\mathbf{v}_i(t + \Delta t) = \mathbf{v}_i(t) + \frac{\mathbf{F}_i(t) + \mathbf{F}_i(t + \Delta t)}{2m_i}\Delta t$$
$$\boldsymbol{\omega}_i(t + \Delta t) = \boldsymbol{\omega}_i(t) + \frac{\mathbf{T}_i(t) + \mathbf{T}_i(t + \Delta t)}{2 I_i}\Delta t$$
Where torque $\mathbf{T}_i = \sum_j (R_i \hat{\mathbf{n}} \times \mathbf{F}_{t,ij})$.


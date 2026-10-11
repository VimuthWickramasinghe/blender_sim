# Scientific & Mathematical Research Repository

This directory contains the theoretical foundations, governing partial differential equations (PDEs), numerical discretizations, and mathematical derivations underlying the simulation engines in **Simulation Assist**.

---

## 📚 Document Index

| Document | Topic | Key Formulations & Physics |
| :--- | :--- | :--- |
| **[01_cfd_mathematics.md](01_cfd_mathematics.md)** | Computational Fluid Dynamics | Navier-Stokes equations, Lattice Boltzmann Method (LBM D2Q9/D3Q19), BGK collision, Chapman-Enskog expansion, boundary bounce-back. |
| **[02_thermal_mathematics.md](02_thermal_mathematics.md)** | Thermal & Thermodynamics | Heat diffusion equation, convective transport, Boussinesq thermal buoyancy, FTCS vs Crank-Nicolson schemes, CFL stability limits. |
| **[03_mechanical_fea_mathematics.md](03_mechanical_fea_mathematics.md)** | Mechanical Stress & FEA | Cauchy stress tensor, infinitesimal strain, 3D Hooke's constitutive law, von Mises yield criterion, Galerkin weak-form stiffness matrix $\mathbf{K}\mathbf{u}=\mathbf{F}$. |
| **[04_robotics_dynamics_mathematics.md](04_robotics_dynamics_mathematics.md)** | Robotics & Multibody Dynamics | $SE(3)$ Lie group kinematics, Geometric Jacobians $\mathbf{J}(\mathbf{q})$, Euler-Lagrange multibody equations $\mathbf{M}\ddot{\mathbf{q}} + \mathbf{C}\dot{\mathbf{q}} + \mathbf{g} = \boldsymbol{\tau}$, actuator PID control. |
| **[05_sph_dem_particle_mathematics.md](05_sph_dem_particle_mathematics.md)** | Particle & Granular Dynamics | SPH smoothing kernels (Cubic spline/Wendland), Tait Equation of State, Monaghan artificial viscosity, DEM Hertzian contact mechanics. |
| **[06_multiphysics_cad_mathematics.md](06_multiphysics_cad_mathematics.md)** | Electromagnetics, Acoustics & CAD | Joule heating, Magnetohydrodynamics (MHD) Lorentz force, Helmholtz acoustics, B-Rep NURBS differential geometry, and conformal tetrahedral Delaunay meshing. |

---

## 🎯 Purpose of this Directory

1. **Mathematical Rigor**: Ensure all computational kernels implemented in `solvers/` match established physical laws and numerical analysis benchmarks.
2. **Community Reference**: Provide open-source scientific documentation so researchers and students using Blender can inspect, cite, and verify formulas.
3. **Validation & Verification (V&V)**: Serve as the ground-truth specification for automated unit tests, convergence rate tests ($O(\Delta x^2), O(\Delta t)$), and conservation verification.


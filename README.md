# Simulation Assist (SimEngine for Blender)

A modular, multi-physics simulation and scientific computing framework integrated directly into Blender. Designed for researchers, engineers, and visual computing scientists who need accurate mathematical simulations (CFD, SPH Particles, Thermal Diffusion, FEA/Stress Analysis) coupled with Blender's photorealistic rendering, headless automation, and automated reporting.

---

## 🔬 Core Capabilities

1. **Multi-Physics & Engineering Solvers via Python & Math Libraries**:
   - **Computational Fluid Dynamics (CFD)**: Lattice Boltzmann Method (LBM), Navier-Stokes solvers, multiphase flows, and aerodynamic drag/lift analysis.
   - **Robotics & Multibody Dynamics (MBD)**: Articulated rigid/flexible chains, URDF/SDF/MJCF import, forward/inverse kinematics (FK/IK), actuator PID control loops, and synthetic sensor emulation (LiDAR, depth camera, IMU).
   - **Mechanical Stress & FEA**: Linear/non-linear elasticity, strain/stress tensors (von Mises), modal vibration, and contact mechanics.
   - **Thermal Simulation**: Conduction, natural/forced convection (Boussinesq), radiation, and phase change.
   - **Particle Dynamics (SPH & DEM)**: Smoothed Particle Hydrodynamics (fluids) and Discrete Element Method (granular sand/powders).
   - **Electromagnetics & Multiphysics**: Joule heating, Magnetohydrodynamics (MHD), and piezoelectric coupling.
   - **Acoustics & Waves**: Helmholtz wave propagation and aeroacoustics.
   - **High-Performance Math Backends**: NumPy, SciPy, Taichi (GPU/CUDA/Vulkan), Numba (JIT), PyTorch/CuPy.

2. **Native CAD Modeling Integration (Roadmap)**:
   - **Exact B-Rep Solid Kernel**: OpenCASCADE Technology (OCCT) engine via CadQuery / build123d.
   - **Standard CAD Formats**: Lossless import/export of STEP (`.stp`, `.step`) and IGES (`.igs`) files.
   - **Parametric Constraint Sketcher**: 2D constraint solving (coincident, tangent, dimensions) and parametric feature trees (extrude, revolve, fillet).
   - **Direct Conformal Meshing**: Automatic tetrahedral/hexahedral meshing directly from CAD solids for FEA/CFD domains (Gmsh/Netgen).

3. **Dedicated Simulation Editor & Custom Node System**:
   - Custom **SimEngine Node Tree** editor directly inside Blender's Node Editor window (`SimNodeTree`).
   - Visually assemble simulation graphs with specialized nodes for domains, solvers (CFD, Heat, SPH, Robotics, FEA), boundary conditions, force fields, and cache exporters.
   - Dedicated one-click **SimEngine Studio Workspace** pairing the 3D Viewport with the Simulation Node Editor, graph monitors, and simulation control deck.

4. **Headless Command-Line Interface (CLI)**:
   - Run complete simulation commissions without opening the Blender GUI.
   - Parameter sweeping, batch experimentation, and reproducible scientific workflows.
   - Remote cluster and workstation execution support.

5. **Blender Data & Viewport Bridge**:
   - Dynamic caching into open formats (OpenVDB, Alembic ABC, PLY, NumPy arrays).
   - Direct mesh attribute binding (Geometry Nodes, vertex colors, velocity vector visualizers, temperature scalar fields).
   - Point cloud and volume generation for real-time viewport preview and instant EEVEE rendering.

6. **Automated Research Reporting & Media Generation (EEVEE Only)**:
   - Ultra-fast batch rendering using **EEVEE** (sub-second per-frame animation export without slow path-tracing bake times).
   - Automated rendering of animation sequences and turntable camera views at 60+ FPS viewport capability.
   - Generation of comprehensive scientific reports (Markdown, HTML, PDF/LaTeX) with loss curves, energy conservation metrics, velocity profiles, and temperature distribution plots.
   - Export of raw simulation datasets (HDF5, CSV, NPZ) for post-processing and peer-review publication.

7. **Google Colab Cloud Processing Bridge**:
   - One-click dispatch of compute-heavy simulations (DEM particles, high-res CFD) to free/Pro Google Colab GPUs (NVIDIA T4 / A100 / L4).
   - Automated packaging of `.simjob` bundles, headless remote execution, and automatic cache retrieval back into Blender for instant EEVEE playback.

---

## 📁 Repository Layout

```text
blender_sim/
├── __init__.py                # Blender Add-on / Extension entry point
├── auto_load.py               # Dynamic module registration system
├── blender_manifest.toml      # Blender 4.2+ extension manifest
├── README.md                  # Project overview and markdown documentation
├── TIMELINE.md                # Development roadmap, phase sequence & Colab bridge
├── SYSTEM_ARCHITECTURE.md     # Detailed architecture and community developer guide
├── colab/                     # Google Colab GPU cloud worker scripts & notebooks
│   └── simengine_worker.ipynb # Headless GPU runner for offloaded simulation baking
├── Research/                  # Theoretical mathematics & PDE derivations repository
│   ├── README.md              # Research document index and physical laws catalog
│   ├── 01_cfd_mathematics.md  # Navier-Stokes, LBM (D2Q9/D3Q19), BGK collision derivations
│   ├── 02_thermal_mathematics.md # Heat diffusion, Boussinesq, Crank-Nicolson, CFL limits
│   ├── 03_mechanical_fea_mathematics.md # Cauchy tensors, 3D Hooke's law, von Mises, FEA weak form
│   ├── 04_robotics_dynamics_mathematics.md # SE(3) Lie group, Jacobians, Euler-Lagrange multibody
│   ├── 05_sph_dem_particle_mathematics.md  # SPH kernels, Tait EOS, DEM Hertzian contact mechanics
│   └── 06_multiphysics_cad_mathematics.md  # Joule heating, MHD, acoustics, NURBS & meshing math
├── nodes/                     # Dedicated In-Blender Custom Node Tree & Sockets
│   ├── __init__.py
│   ├── node_tree.py           # Custom SimNodeTree registration
│   ├── solver_nodes.py        # CFD, Thermal, Particle, and FEA nodes
│   ├── boundary_nodes.py      # Inflow, Outflow, Wall, and Dirichlet/Neumann nodes
│   └── evaluator.py           # Node graph to simulation config compiler
├── cli/                       # Command-line interface & automation runners
│   ├── __init__.py
│   ├── commission.py          # Job runner, parameter sweeps, headless worker
│   └── report_generator.py    # Scientific data analysis and PDF/Markdown reports
├── solvers/                   # Physics solvers and numerical calculation core
│   ├── __init__.py
│   ├── base_solver.py         # Abstract base class for all simulation engines
│   ├── cfd_lbm.py             # CFD solver (Lattice Boltzmann / Navier-Stokes)
│   ├── thermal_diff.py        # Heat transfer and thermal diffusion solver
│   └── particle_sph.py        # SPH particle dynamics solver
├── blender_bridge/            # Blender integration, caching, and visualizers
│   ├── __init__.py
│   ├── cache_manager.py       # OpenVDB/Alembic/NPZ disk cache management
│   ├── mesh_attributes.py     # Vertex attributes, color ramps, vector fields
│   └── camera_render.py       # Camera setup, light staging, and batch rendering
└── ui/                        # Blender UI panels, operators, workspace and properties
    ├── __init__.py
    ├── panels.py              # Sidebar (N-panel) controls for parameters
    ├── workspace.py           # Dedicated SimEngine Workspace layout generator
    └── operators.py           # Operators to bake, run, and export from Blender UI
```

---

## 🚀 Quickstart & CLI Commissioning

### 1. Requirements
- Blender 4.2 LTS or newer
- Python 3.10+ (Blender bundled Python or system environment)
- Core Python libraries:
  ```bash
  pip install numpy scipy matplotlib meshio h5py
  ```
  *(Optional GPU acceleration: `pip install taichi numba`)*

### 2. Running Simulations via Command Line (Headless)
Run a thermal diffusion commission and automatically render frames:
```bash
python -m cli.commission --solver thermal --config experiments/heat_sink.json --steps 200 --render --report
```

Or trigger headless via Blender's Python runtime:
```bash
blender -b -P run_sim.py -- --solver cfd --resolution 128 --timesteps 500 --output ./output/cfd_run1
```

### 3. Running Inside Blender GUI
1. Install or load this folder as a Blender extension/addon via `Preferences > Add-ons > Install`.
2. Open the 3D Viewport sidebar (`N` panel) and navigate to **SimEngine**.
3. Select the target mesh domain and physics solver (CFD / Thermal / SPH).
4. Configure physics constants (viscosity, Reynolds number, thermal diffusivity).
5. Click **Bake Simulation** to visualize frame-by-frame with Geometry Nodes or Particle Cloud shaders.

---

## 📊 Scientific Reporting & Research Output

When triggered with `--report`, the simulation system automatically tracks:
- Computational time and step convergence.
- Physical invariants (mass conservation, total thermal energy, momentum balance).
- Cross-sectional scalar/vector slices rendered via Matplotlib.
- Output compiled into `report.html` and `report.md` alongside high-res rendered animation frames (`.mp4` / `.png` sequences).

---

## 🛠️ Contributing & Developer Guide

Refer to [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) for full technical documentation on:
- How solver abstractions communicate with Blender's dependency graph.
- How to implement a new custom PDE solver.
- Memory handling, caching, and GPU buffer interop.

# Mathematical Foundations: Robotics & Multibody Dynamics (MBD)

This document formalizes the rigid/flexible body kinematics, differential geometry of rotations, equations of motion, and control systems implemented in the robotics simulation module.

---

## 1. Spatial Kinematics & Lie Group Representations

### 1.1 Special Orthogonal Group $SO(3)$
Orientation of a rigid frame $\{B\}$ relative to reference frame $\{A\}$ is represented by an orthogonal matrix $\mathbf{R} \in SO(3)$:
$$\mathbf{R}^T \mathbf{R} = \mathbf{I}, \quad \det(\mathbf{R}) = +1$$

#### Unit Quaternion Representation ($\mathbf{q}_{quat} \in \mathbb{H}, \|\mathbf{q}_{quat}\| = 1$):
$$\mathbf{q}_{quat} = \begin{bmatrix} \eta & \boldsymbol{\epsilon}^T \end{bmatrix}^T = \left[ \cos(\theta/2), \hat{\mathbf{k}} \sin(\theta/2) \right]^T$$
Rotation operator without gimbal lock singularities:
$$\mathbf{R}(\mathbf{q}_{quat}) = (\eta^2 - \|\boldsymbol{\epsilon}\|^2)\mathbf{I} + 2 \boldsymbol{\epsilon} \boldsymbol{\epsilon}^T + 2\eta [\boldsymbol{\epsilon}]_\times$$
Where $[\boldsymbol{\epsilon}]_\times$ is the skew-symmetric cross-product matrix.

### 1.2 Special Euclidean Group $SE(3)$
Homogeneous transformation matrix $\mathbf{T} \in SE(3)$:
$$\mathbf{T} = \begin{bmatrix} \mathbf{R} & \mathbf{p} \\ \mathbf{0}^T & 1 \end{bmatrix} \in \mathbb{R}^{4 \times 4}$$

---

## 2. Forward & Differential Kinematics

For an open kinematic chain with $n$ degrees of freedom and generalized joint coordinates $\mathbf{q} = [q_1, q_2, \dots, q_n]^T \in \mathbb{R}^n$:

### 2.1 Product of Exponentials (PoE) Formulation
$$\mathbf{T}_{0n}(\mathbf{q}) = e^{[\mathcal{S}_1] q_1} e^{[\mathcal{S}_2] q_2} \cdots e^{[\mathcal{S}_n] q_n} \mathbf{T}_{0n}(\mathbf{0})$$
Where $\mathcal{S}_i = [\boldsymbol{\omega}_i^T, \mathbf{v}_i^T]^T \in \mathbb{R}^6$ represents the screw axis in spatial frame coordinates.

### 2.2 Geometric Jacobian Matrix
Relates joint velocities $\dot{\mathbf{q}}$ to end-effector spatial twist $\mathbf{V}_e = [\boldsymbol{\omega}_e^T, \mathbf{v}_e^T]^T \in \mathbb{R}^6$:
$$\mathbf{V}_e = \mathbf{J}(\mathbf{q}) \dot{\mathbf{q}}$$

Where the $i$-th column $\mathbf{J}_i$ for revolute joint $i$:
$$\mathbf{J}_i(\mathbf{q}) = \begin{bmatrix} \hat{\mathbf{z}}_{i-1} \\ \hat{\mathbf{z}}_{i-1} \times (\mathbf{p}_e - \mathbf{p}_{i-1}) \end{bmatrix}$$
And for prismatic joint $i$:
$$\mathbf{J}_i(\mathbf{q}) = \begin{bmatrix} \mathbf{0} \\ \hat{\mathbf{z}}_{i-1} \end{bmatrix}$$

### 2.3 Inverse Kinematics (IK)
For target spatial velocity $\mathbf{V}_{desired}$:
$$\dot{\mathbf{q}} = \mathbf{J}^{\dagger} \mathbf{V}_{desired} + (\mathbf{I} - \mathbf{J}^{\dagger}\mathbf{J}) \dot{\mathbf{q}}_{null}$$
Where $\mathbf{J}^{\dagger} = \mathbf{J}^T (\mathbf{J} \mathbf{J}^T + \lambda^2 \mathbf{I})^{-1}$ is the Damped Least Squares (DLS / Levenberg-Marquardt) pseudo-inverse avoiding kinematic singularities.

---

## 3. Multibody Dynamics: Equations of Motion

### 3.1 Euler-Lagrange Formulation
The Lagrangian of the articulated mechanical system:
$$\mathcal{L}(\mathbf{q}, \dot{\mathbf{q}}) = \mathcal{K}(\mathbf{q}, \dot{\mathbf{q}}) - \mathcal{P}(\mathbf{q})$$
Where kinetic energy $\mathcal{K} = \frac{1}{2} \dot{\mathbf{q}}^T \mathbf{M}(\mathbf{q}) \dot{\mathbf{q}}$ and potential energy $\mathcal{P}(\mathbf{q}) = \sum_i m_i g h_i(\mathbf{q})$.

Applying the Euler-Lagrange equation $\frac{d}{dt} \frac{\partial \mathcal{L}}{\partial \dot{\mathbf{q}}} - \frac{\partial \mathcal{L}}{\partial \mathbf{q}} = \boldsymbol{\tau}$:
$$\mathbf{M}(\mathbf{q}) \ddot{\mathbf{q}} + \mathbf{C}(\mathbf{q}, \dot{\mathbf{q}}) \dot{\mathbf{q}} + \mathbf{g}(\mathbf{q}) + \mathbf{J}_c^T \mathbf{f}_c = \boldsymbol{\tau} - \mathbf{B}_f \dot{\mathbf{q}}$$

Where:
- $\mathbf{M}(\mathbf{q}) \in \mathbb{R}^{n \times n}$ is the symmetric positive-definite Mass / Inertia matrix.
- $\mathbf{C}(\mathbf{q}, \dot{\mathbf{q}}) \dot{\mathbf{q}} \in \mathbb{R}^n$ represents Coriolis and centrifugal generalized forces.
  Christoffel symbols of the first kind:
  $$C_{kj} = \sum_{i=1}^n \frac{1}{2} \left( \frac{\partial M_{kj}}{\partial q_i} + \frac{\partial M_{ki}}{\partial q_j} - \frac{\partial M_{ij}}{\partial q_k} \right) \dot{q}_i$$
- $\mathbf{g}(\mathbf{q}) = \frac{\partial \mathcal{P}}{\partial \mathbf{q}} \in \mathbb{R}^n$ is the gravitational generalized torque vector.
- $\mathbf{J}_c^T \mathbf{f}_c$ is the contact wrench projected into joint space.
- $\boldsymbol{\tau}$ is the control actuator torque vector.
- $\mathbf{B}_f$ is the viscous joint damping matrix.

---

## 4. Actuator Models & Control Systems

### 4.1 DC Motor Dynamics with Back-EMF
Torque output $\tau_m$ governed by armature voltage $V_a$ and gear ratio $N_g$:
$$V_a = R_a i_a + L_a \frac{di_a}{dt} + K_b (N_g \dot{q})$$
$$\tau = N_g K_t i_a - \tau_{friction}$$
Where $K_t$ is motor torque constant, $K_b$ is back-EMF constant.

### 4.2 Computed Torque Control + PID
To track a reference trajectory $\mathbf{q}_d(t)$:
$$\boldsymbol{\tau} = \mathbf{M}(\mathbf{q}) \left[ \ddot{\mathbf{q}}_d + \mathbf{K}_p (\mathbf{q}_d - \mathbf{q}) + \mathbf{K}_d (\dot{\mathbf{q}}_d - \dot{\mathbf{q}}) + \mathbf{K}_i \int (\mathbf{q}_d - \mathbf{q}) dt \right] + \mathbf{C}(\mathbf{q}, \dot{\mathbf{q}})\dot{\mathbf{q}} + \mathbf{g}(\mathbf{q})$$
Linearizes error dynamics into asymptotically stable second-order system:
$$\ddot{\mathbf{e}} + \mathbf{K}_d \dot{\mathbf{e}} + \mathbf{K}_p \mathbf{e} + \mathbf{K}_i \int \mathbf{e} \, dt = \mathbf{0}$$


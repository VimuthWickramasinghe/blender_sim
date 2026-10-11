"""SimEngine Custom Node Editor Tree and Viewport Integration.

Defines the custom SimNodeTree, physical node sockets, core DEM nodes,
and topbar viewport integration.
"""

import bpy


# -----------------------------------------------------------------------------
# 1. Custom Node Tree Definition
# -----------------------------------------------------------------------------
class SimEngineNodeTree(bpy.types.NodeTree):
    """Custom Node Tree for Visual Simulation Assembly."""

    bl_idname = "SimEngineNodeTree"
    bl_label = "SimEngine Simulation Nodes"
    bl_icon = "PHYSICS"


# -----------------------------------------------------------------------------
# 2. Custom Node Sockets
# -----------------------------------------------------------------------------
class SimSocketDomain(bpy.types.NodeSocket):
    """Socket transmitting 3D simulation bounds & resolution."""

    bl_idname = "SimSocketDomain"
    bl_label = "Simulation Domain"

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.35, 0.7, 0.9, 1.0)  # Light cyan


class SimSocketParticles(bpy.types.NodeSocket):
    """Socket transmitting DEM particle state."""

    bl_idname = "SimSocketParticles"
    bl_label = "Particle Data"

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.9, 0.65, 0.2, 1.0)  # Amber / Gold


class SimSocketPhysics(bpy.types.NodeSocket):
    """Socket transmitting physical material properties."""

    bl_idname = "SimSocketPhysics"
    bl_label = "Physics Properties"

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.4, 0.85, 0.45, 1.0)  # Green


# -----------------------------------------------------------------------------
# 3. Custom Node Items
# -----------------------------------------------------------------------------
class SimNodeDomain(bpy.types.Node):
    """Node defining the physical bounding domain and spatial discretization."""

    bl_idname = "SimNodeDomain"
    bl_label = "Simulation Domain"
    bl_icon = "MESH_CUBE"

    domain_size: bpy.props.FloatVectorProperty(
        name="Size (m)",
        description="Bounding box dimensions in meters",
        default=(2.0, 2.0, 2.0),
        min=0.01,
    )

    voxel_res: bpy.props.IntProperty(
        name="Grid Cells",
        description="Spatial grid resolution per axis",
        default=64,
        min=8,
        max=1024,
    )

    def init(self, context):
        self.outputs.new("SimSocketDomain", "Domain")

    def draw_buttons(self, context, layout):
        col = layout.column(align=True)
        col.prop(self, "domain_size")
        col.prop(self, "voxel_res")


class SimNodeDEMEmitter(bpy.types.Node):
    """Node generating granular DEM particles."""

    bl_idname = "SimNodeDEMEmitter"
    bl_label = "DEM Particle Emitter"
    bl_icon = "MOD_PARTICLES"

    particle_count: bpy.props.IntProperty(
        name="Count",
        description="Total particles emitted",
        default=5000,
        min=10,
        max=5000000,
    )

    particle_radius: bpy.props.FloatProperty(
        name="Radius (m)",
        description="Mean particle radius",
        default=0.005,
        min=0.0001,
        precision=4,
    )

    particle_density: bpy.props.FloatProperty(
        name="Density (kg/m³)",
        description="Solid material density",
        default=2500.0,
        min=1.0,
    )

    def init(self, context):
        self.outputs.new("SimSocketParticles", "Particles")

    def draw_buttons(self, context, layout):
        col = layout.column(align=True)
        col.prop(self, "particle_count")
        col.prop(self, "particle_radius")
        col.prop(self, "particle_density")


class SimNodeDEMPhysics(bpy.types.Node):
    """Node configuring contact mechanics, friction, and caking."""

    bl_idname = "SimNodeDEMPhysics"
    bl_label = "DEM Contact & Caking"
    bl_icon = "FORCE_FORCE"

    youngs_modulus: bpy.props.FloatProperty(
        name="Young's Modulus (Pa)",
        default=1e7,
        min=1e3,
    )

    restitution: bpy.props.FloatProperty(
        name="Restitution (e)",
        default=0.7,
        min=0.0,
        max=1.0,
    )

    sliding_friction: bpy.props.FloatProperty(
        name="Friction (μs)",
        default=0.4,
        min=0.0,
        max=2.0,
    )

    enable_thermal_caking: bpy.props.BoolProperty(
        name="Thermal Caking",
        description="Enable temperature-driven agglomeration and sintering",
        default=True,
    )

    def init(self, context):
        self.outputs.new("SimSocketPhysics", "Contact Physics")

    def draw_buttons(self, context, layout):
        col = layout.column(align=True)
        col.prop(self, "youngs_modulus")
        col.prop(self, "restitution")
        col.prop(self, "sliding_friction")
        col.prop(self, "enable_thermal_caking")


class SimNodeBakeOutput(bpy.types.Node):
    """Node receiving assembled physics graph and executing simulation bake."""

    bl_idname = "SimNodeBakeOutput"
    bl_label = "SimEngine Output & Bake"
    bl_icon = "PLAY"

    time_steps: bpy.props.IntProperty(
        name="Time Steps",
        default=250,
        min=1,
    )

    time_delta: bpy.props.FloatProperty(
        name="dt (s)",
        default=0.001,
        min=0.00001,
        precision=5,
    )

    use_gpu: bpy.props.BoolProperty(
        name="GPU Acceleration",
        default=True,
    )

    def init(self, context):
        self.inputs.new("SimSocketDomain", "Domain")
        self.inputs.new("SimSocketParticles", "Particles")
        self.inputs.new("SimSocketPhysics", "Physics")

    def draw_buttons(self, context, layout):
        col = layout.column(align=True)
        col.prop(self, "time_steps")
        col.prop(self, "time_delta")
        col.prop(self, "use_gpu", toggle=True)
        layout.separator()
        layout.operator("simengine.bake_simulation", text="Bake Node Graph", icon="PLAY")


# -----------------------------------------------------------------------------
# 4. Viewport Top Header Integration (Fast Control in 3D Viewport)
# -----------------------------------------------------------------------------
class SIMENGINE_MT_viewport_menu(bpy.types.Menu):
    """SimEngine Header Dropdown Menu in the 3D Viewport."""

    bl_idname = "SIMENGINE_MT_viewport_menu"
    bl_label = "SimEngine"

    def draw(self, context):
        layout = self.layout
        layout.operator("simengine.create_workspace", text="Switch to SimEngine Studio", icon="WORKSPACE")
        layout.separator()
        layout.operator("simengine.bake_simulation", text="Bake Simulation", icon="PLAY")
        layout.operator("simengine.render_video", text="Render EEVEE Video", icon="FILE_MOVIE")
        layout.operator("simengine.generate_report", text="Export Dynamic HTML Report", icon="DOCUMENTS")


class SIMENGINE_OT_create_workspace(bpy.types.Operator):
    """Operator to switch or set up a dedicated Simulation Studio workspace."""

    bl_idname = "simengine.create_workspace"
    bl_label = "Setup SimEngine Workspace"
    bl_description = "Configure viewports for simulation nodes and 3D visualization"
    bl_options = {"REGISTER"}

    def execute(self, context):
        self.report({"INFO"}, "SimEngine: Simulation Studio Workspace activated.")
        return {"FINISHED"}


def draw_viewport_header(self, context):
    """Draws the SimEngine menu in the 3D Viewport top header."""
    layout = self.layout
    layout.menu("SIMENGINE_MT_viewport_menu", text="SimEngine", icon="PHYSICS")


# -----------------------------------------------------------------------------
# Registration
# -----------------------------------------------------------------------------
classes = (
    SimEngineNodeTree,
    SimSocketDomain,
    SimSocketParticles,
    SimSocketPhysics,
    SimNodeDomain,
    SimNodeDEMEmitter,
    SimNodeDEMPhysics,
    SimNodeBakeOutput,
    SIMENGINE_MT_viewport_menu,
    SIMENGINE_OT_create_workspace,
)


def register():
    # Append top menu into 3D Viewport header
    bpy.types.VIEW3D_HT_header.append(draw_viewport_header)


def unregister():
    # Remove top menu from 3D Viewport header
    bpy.types.VIEW3D_HT_header.remove(draw_viewport_header)


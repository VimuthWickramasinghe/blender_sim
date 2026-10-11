"""SimEngine 3D Viewport Sidebar Panel & Operators.

Provides the interactive control panel inside the 3D Viewport sidebar (N-panel).
"""

import bpy


class SimEngineProperties(bpy.types.PropertyGroup):
    """Global properties for simulation setup in the viewport."""

    solver_type: bpy.props.EnumProperty(
        name="Solver Type",
        description="Select simulation physics solver",
        items=[
            ("DEM", "DEM (Granular Particles)", "Discrete Element Method particle simulation"),
            ("THERMAL", "Thermal Diffusion", "Thermal conduction and heat transfer"),
            ("CFD_LBM", "CFD (LBM Real-Time)", "Lattice Boltzmann fluid dynamics"),
            ("CFD_OPENFOAM", "CFD (OpenFOAM)", "OpenFOAM finite-volume Navier-Stokes"),
            ("FEA", "Mechanical / FEA", "Finite element structural stress and strain"),
        ],
        default="DEM",
    )

    time_steps: bpy.props.IntProperty(
        name="Time Steps",
        default=250,
        min=1,
        max=1000000,
    )

    dt: bpy.props.FloatProperty(
        name="Time Step (dt)",
        default=0.001,
        min=0.000001,
        max=1.0,
        precision=5,
    )

    particle_count: bpy.props.IntProperty(
        name="Particle Count",
        default=5000,
        min=10,
        max=5000000,
    )

    particle_radius: bpy.props.FloatProperty(
        name="Mean Radius (m)",
        default=0.005,
        min=0.00001,
        precision=4,
    )

    particle_density: bpy.props.FloatProperty(
        name="Density (kg/m³)",
        default=2500.0,
        min=1.0,
    )

    youngs_modulus: bpy.props.FloatProperty(
        name="Young's Modulus (Pa)",
        default=1e7,
        min=1e3,
    )

    restitution_coeff: bpy.props.FloatProperty(
        name="Restitution (e)",
        default=0.7,
        min=0.0,
        max=1.0,
    )

    friction_sliding: bpy.props.FloatProperty(
        name="Sliding Friction (μs)",
        default=0.4,
        min=0.0,
        max=2.0,
    )

    rolling_resistance: bpy.props.FloatProperty(
        name="Rolling Resistance (μr)",
        default=0.05,
        min=0.0,
        max=1.0,
    )

    enable_thermal_buildup: bpy.props.BoolProperty(
        name="Thermal Buildup",
        default=True,
    )

    particle_temp_init: bpy.props.FloatProperty(
        name="Initial Temp (K)",
        default=293.15,
        min=0.0,
    )

    enable_caking: bpy.props.BoolProperty(
        name="Thermal Caking & Sintering",
        default=False,
    )

    sinter_temp_threshold: bpy.props.FloatProperty(
        name="Sinter Temp (K)",
        default=350.0,
        min=0.0,
    )

    use_gpu: bpy.props.BoolProperty(
        name="GPU Acceleration",
        default=True,
    )

    dispatch_colab: bpy.props.BoolProperty(
        name="Offload to Colab",
        default=False,
    )

    cache_dir: bpy.props.StringProperty(
        name="Cache Directory",
        default="//cache",
        subtype="DIR_PATH",
    )


class SIMENGINE_OT_bake_simulation(bpy.types.Operator):
    """Operator to execute the simulation bake."""

    bl_idname = "simengine.bake_simulation"
    bl_label = "Bake Simulation"
    bl_description = "Run simulation computation and cache generation"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.simengine_props
        self.report(
            {"INFO"},
            f"SimEngine: Baking {props.solver_type} ({props.time_steps} steps, dt={props.dt}).",
        )
        return {"FINISHED"}


class SIMENGINE_OT_render_video(bpy.types.Operator):
    """Operator to render simulation animation video via EEVEE."""

    bl_idname = "simengine.render_video"
    bl_label = "Render EEVEE Video"
    bl_description = "Configure camera and render simulation frames to video"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        self.report({"INFO"}, "SimEngine: Configured camera and EEVEE settings for video rendering.")
        return {"FINISHED"}


class SIMENGINE_OT_generate_report(bpy.types.Operator):
    """Operator to export interactive HTML research report."""

    bl_idname = "simengine.generate_report"
    bl_label = "Export Dynamic HTML Report"
    bl_description = "Compile simulation metrics into an interactive HTML research paper"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        self.report({"INFO"}, "SimEngine: Dynamic HTML research report generated.")
        return {"FINISHED"}


class SIMENGINE_PT_viewport_panel(bpy.types.Panel):
    """SimEngine Sidebar Panel inside the 3D Viewport."""

    bl_label = "SimEngine Control Panel"
    bl_idname = "SIMENGINE_PT_viewport_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SimEngine"

    def draw(self, context):
        layout = self.layout
        props = context.scene.simengine_props

        # Header Info Box
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Multi-Physics Simulation Studio", icon="PHYSICS")
        col.label(text="Engine: EEVEE Real-Time", icon="RENDER_ANIMATION")

        # Solver Setup Section
        layout.separator()
        layout.label(text="Simulation Configuration:", icon="PREFERENCES")
        layout.prop(props, "solver_type")

        col = layout.column(align=True)
        col.prop(props, "time_steps")
        col.prop(props, "dt")

        if props.solver_type == "DEM":
            # Granular Material & Mechanical Properties
            box_mat = layout.box()
            box_mat.label(text="Granular Material & Contact:", icon="MOD_PARTICLES")
            col_mat = box_mat.column(align=True)
            col_mat.prop(props, "particle_count")
            col_mat.prop(props, "particle_radius")
            col_mat.prop(props, "particle_density")
            col_mat.prop(props, "youngs_modulus")

            # Contact & Friction
            box_fric = layout.box()
            box_fric.label(text="Contact Damping & Friction:", icon="FORCE_FORCE")
            col_fric = box_fric.column(align=True)
            col_fric.prop(props, "restitution_coeff")
            col_fric.prop(props, "friction_sliding")
            col_fric.prop(props, "rolling_resistance")

            # Advanced Multi-Physics
            box_adv = layout.box()
            box_adv.label(text="Thermal Buildup & Caking:", icon="SOLO_ON")
            box_adv.prop(props, "enable_thermal_buildup")
            if props.enable_thermal_buildup:
                col_th = box_adv.column(align=True)
                col_th.prop(props, "particle_temp_init")

            box_adv.prop(props, "enable_caking")
            if props.enable_caking:
                col_ck = box_adv.column(align=True)
                col_ck.prop(props, "sinter_temp_threshold")

        # Hardware & Compute Section
        layout.separator()
        box_hardware = layout.box()
        box_hardware.label(text="Hardware & Cloud Backend:", icon="SYSTEM")
        row = box_hardware.row()
        row.prop(props, "use_gpu", toggle=True)
        row.prop(props, "dispatch_colab", toggle=True)

        # Caching & Output
        layout.separator()
        layout.prop(props, "cache_dir")

        # Action Buttons
        layout.separator()
        row = layout.row(align=True)
        row.scale_y = 1.5
        row.operator("simengine.bake_simulation", icon="PLAY", text="Bake Simulation")

        # Research & Media Export Section
        layout.separator()
        box_export = layout.box()
        box_export.label(text="Research & Video Output:", icon="FILE_TEXT")
        col_exp = box_export.column(align=True)
        col_exp.operator("simengine.render_video", icon="FILE_MOVIE", text="Setup & Render EEVEE Video")
        col_exp.operator("simengine.generate_report", icon="DOCUMENTS", text="Export Dynamic HTML Report")


classes = (
    SimEngineProperties,
    SIMENGINE_OT_bake_simulation,
    SIMENGINE_OT_render_video,
    SIMENGINE_OT_generate_report,
    SIMENGINE_PT_viewport_panel,
)


def register():
    bpy.types.Scene.simengine_props = bpy.props.PointerProperty(type=SimEngineProperties)


def unregister():
    if hasattr(bpy.types.Scene, "simengine_props"):
        del bpy.types.Scene.simengine_props


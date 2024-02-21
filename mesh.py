from pyvistaqt import BackgroundPlotter


class MeshPlotter:
    def __init__(self):
        self.plotter = BackgroundPlotter()
        self.plotter.set_background("grey")
        self.DENSITY_THRESHOLD = .0002
        self.largest_cluster_centers = None
        self.densities = None
        self.mesh = None
        self.meshes = []  # A list to store multiple mesh objects
        self.heatmap_actor = None
        self.cell_list = []
        self.is_toggled = False

mesh_plotter = MeshPlotter()

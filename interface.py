from sys import path
from add_remove_files import erase_heatmap_points, add_mesh
from mesh import mesh_plotter
path.append('.\\Connection')
from PyQt5.QtWidgets import QAction


def add_action(toolbar, text, method):
    action = QAction(text)
    action.triggered.connect(method)
    toolbar.addAction(text).triggered.connect(method)
    return
def add_toggle():
    if mesh_plotter.is_toggled:
        mesh_plotter.is_toggled = False
        mesh_plotter.heatmap_actor = mesh_plotter.plotter.add_points(mesh_plotter.largest_cluster_centers, scalars=mesh_plotter.densities, cmap='blue', point_size=10)
        mesh_plotter.plotter.add_mesh(mesh_plotter.mesh, show_edges=True, line_width=.5)
        add_myfeatures()
    else:
        mesh_plotter.is_toggled = True
        erase_heatmap_points()
        if mesh_plotter.densities is not None:
            high_density_indices = mesh_plotter.densities > mesh_plotter.DENSITY_THRESHOLD
            if high_density_indices.any():
                mesh_plotter.plotter.add_points(mesh_plotter.largest_cluster_centers[high_density_indices], scalars=mesh_plotter.densities[high_density_indices], cmap='blue', point_size=10)
                add_myfeatures()
            else:
                print("No points found with density above threshold.")
                print("Densities:", mesh_plotter.densities)
        else:
            print("No points found for the specified cluster.")
def add_myfeatures():
    user_menu = mesh_plotter.plotter.main_menu.addMenu('My Features')

    user_menu.addAction('Add Mesh', add_mesh)

    if mesh_plotter.is_toggled:
        user_menu.addAction('Show cell', add_toggle)
    else:
        user_menu.addAction('Show soma', add_toggle)
def add_widget():
    user_toolbar = mesh_plotter.plotter.app_window.addToolBar('User Toolbar')
    add_action(user_toolbar, 'Line Widget', mesh_plotter.plotter.add_line_widget)
def render():
    add_myfeatures()
    add_widget()
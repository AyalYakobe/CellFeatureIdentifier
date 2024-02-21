from sys import path
from calculations import count_disconnected_components, extract_and_expand_cluster
from mesh import mesh_plotter
path.append('.\\Connection')
from PyQt5.QtWidgets import QFileDialog
import pyvista as pv



def erase_heatmap_points():
    if mesh_plotter.heatmap_actor is not None:
        mesh_plotter.plotter.remove_actor(mesh_plotter.heatmap_actor)
        mesh_plotter.heatmap_actor = None
def add_mesh():
    options = QFileDialog.Options()
    filePath, _ = QFileDialog.getOpenFileName(None, "Open Mesh File", "", "Mesh files (*.obj *.mtl);;OFF files (*.off)", options=options)

    if filePath:  # If a file was selected
        mesh_data = load_mesh(filePath)

        if mesh_data is not None:
            largest_cluster_centers, densities, mesh = mesh_data

            # Append the mesh and its data to the list of meshes
            mesh_plotter.meshes.append((largest_cluster_centers, densities, mesh))

            # For each mesh, plot it along with its heatmap points
            for largest_cluster_centers, densities, mesh in mesh_plotter.meshes:
                # Check if densities are not None to plot
                if densities is not None:
                    mesh_plotter.plotter.add_points(largest_cluster_centers, scalars=densities, cmap='blue', point_size=10)
                mesh_plotter.plotter.add_mesh(mesh, show_edges=True, line_width=.5)

            mesh_plotter.plotter.show()
def load_mesh(dialogue_results):
    file_path = dialogue_results

    if file_path:
        mesh = pv.read(file_path)
        number_of_vessels = count_disconnected_components(mesh)
        print(f"Number of disconnected vessels: {number_of_vessels}")
        largest_cluster_centers, densities = extract_and_expand_cluster(mesh)
        if densities is not None:
            return largest_cluster_centers, densities, mesh
    else:
        print("No points found for the specified cluster.")
        return None
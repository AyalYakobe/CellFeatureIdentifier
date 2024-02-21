from sys import path
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import kde
path.append('.\\Connection')


def extract_and_expand_cluster(mesh, bandwidth=0.01):
    # Extract the centers of all edges in the mesh
    edge_centers = mesh.extract_all_edges().cell_centers().points

    # Check if there are enough points for density estimation
    if len(edge_centers) > 1:
        # Apply KDE to all edge centers. Assuming the mesh is 3D, we still project to 2D for visualization
        k = kde.gaussian_kde(edge_centers[:, :2].T, bw_method=bandwidth)
        densities = k(edge_centers[:, :2].T)
    else:
        print("Not enough points for density estimation.")
        densities = None

    return edge_centers, densities
def plot_density(mesh, bandwidth=0.2, resolution=100):
    points = mesh.points
    x, y = points[:, 0], points[:, 1]

    k = kde.gaussian_kde([x, y], bw_method=bandwidth)
    xi, yi = np.mgrid[x.min():x.max():resolution*1j, y.min():y.max():resolution*1j]
    zi = k(np.vstack([xi.flatten(), yi.flatten()]))
    zi = zi.reshape(xi.shape)

    plt.pcolormesh(xi, yi, zi, shading='auto')
    plt.colorbar(label='Density')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()
def find_center(mesh, largest_cluster, density, eps=0.5, min_samples=4, bandwidth=0.2, density_threshold=0.5):
    if mesh is not None:
        largest_cluster_centers, densities = largest_cluster, density

        if densities is not None:
            center_point = largest_cluster_centers[np.argmax(densities)]
            return center_point
        else:
            return np.mean(mesh.points, axis=0)
def count_disconnected_components(mesh):
    """
    Counts the number of disconnected components in a given mesh by analyzing connectivity.

    Parameters:
    - mesh: A PyVista mesh object.

    Returns:
    - int: The number of disconnected components in the mesh.
    """
    # Apply the connectivity filter to identify disconnected components
    connected_components = mesh.connectivity(largest=True)

    # Access the scalar data correctly to get the labels
    # Ensure compatibility with different PyVista versions
    if hasattr(connected_components, 'point_data'):
        # For newer versions of PyVista
        labels = connected_components.point_data.get_array('RegionId')
    elif hasattr(connected_components, 'point_arrays'):
        # Fallback for older versions or different attribute naming
        labels = connected_components.point_arrays.get('RegionId')
    else:
        raise AttributeError("Unable to access point data for RegionId.")

    # If labels is None, it means 'RegionId' was not found; handle this case
    if labels is None:
        raise ValueError("RegionId not found in point data. Ensure connectivity analysis is correct.")

    # Count unique labels to determine the number of components
    number_of_components = len(np.unique(labels))

    return number_of_components

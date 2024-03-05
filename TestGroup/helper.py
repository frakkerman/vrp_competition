import numpy as np
import random

# an example file, you can use more submodules like this to keep your code readable, but import them in main.py


def parse_instance(instance_dict):
    """Parse the instance dictionary to extract node coordinates."""
    node_coords = np.array(instance_dict['node_coord'])
    return node_coords


def generate_random_routes(indices, min_size=1, max_size=5):
    routes = []
    while indices:
        size = random.randint(min_size,
                              min(max_size, len(indices)))  # Ensure the size is within the remaining indices
        route = indices[:size]
        routes.append(route)
        indices = indices[size:]
    return routes

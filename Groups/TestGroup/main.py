import vrplib
import numpy as np
import scipy
import pandas as pd
import os
import sys
import random
# Get the directory of the currently executing script (main.py)
current_script_directory = os.path.dirname(os.path.realpath(__file__))
# Construct the path to helper.py relative to the current script
helper_module_path = os.path.join(current_script_directory, 'helper.py')
# Add the directory containing main.py to sys.path to enable imports
sys.path.append(current_script_directory)
# Now you can import helper.py
import helper

# These are the libraries we provide by default. If you want to use different Python libraries:
# please let us know so that we can look if these can be added to the competition environment.
# Note: importing a library that is not listed above will result in an error when submitting your code


def main(instance):
    """
    This is the starting point of the code, you need to design a main function that has these args and returns
     Args:
        instance (vrplib): instance in vrplib format
    Returns:
        solution (vrplib): solution in vrplib format.
    """

    # Example operation on the instance
    print(instance.keys())

    # obtain the coordinates of customers. Note that index=0 is the depot
    # in your solution, you do not need to include the start and finish at the depot, as it is
    # implicitly assumed that all vehicles start and end at the depot
    coords = helper.parse_instance(instance)

    # remove depot from list
    coords = coords[1:, :]

    # For this example, we implement a function that returns a random route. It is your task to come up
    # with a better approach to reduce the total distance covered
    n_customers = coords.shape[0]  # Number of customers

    # Generate a list of all customer indices
    customer_indices = list(range(1, n_customers + 1))  # Starting from 1 to n_customers

    # Shuffle the customer indices to randomize the route
    random.shuffle(customer_indices)

    # Generate the random routes, you should come upt with something better...
    random_routes = helper.generate_random_routes(customer_indices)

    # Create the solution dictionary
    solution = {'routes': random_routes}
    print('Random sequence solution')
    print(solution)

    # students should implement logic to generate the solution, it is not enough to just provide the solution sequence
    # NOTE: please remove all loading, writing, and print statements from your submission code

    return solution  # you need to return a solution in this exact (vrplib) format

# NOTE: comment out all the below lines before submission, this code is only useful for locally running your code,
# but will yield errors when submitting


# if __name__ == "__main__":
#     # Read VRPLIB formatted instances, here you can read any instance you want locally
#     instance = vrplib.read_instance("../../Instances/Test/X-n101-k25.vrp")
#     sol = main(instance)

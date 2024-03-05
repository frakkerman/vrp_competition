import vrplib
import os
import sys
import random
import argparse
""""
These are the libraries we provide by default. If you want to use different Python libraries:
please let us know so that we can look if these can be added to the competition environment.
Note: importing a library that is not listed above will result in an error when running your code on the server!
"""

# below we import the "helper" submodule, see "helper.py"
# you can add more submodules in this same way, if needed
import helper


def main(instance):
    """
    This is the starting point of the code, you need to design a main function that has these args and returns
     Args:
        instance (vrplib): instance in vrplib format
    Returns:
        solution (vrplib): solution in vrplib format.
    """

    print('\nPlease change the folder name "TestGroup" into your own group name, e.g., "Group1"\n')

    # Example operation on the instance
    print(instance.keys())

    # obtain the coordinates of customers. Note that index=0 is the depot
    # in your solution, you do not need to include the start and finish at the depot, as it is
    # implicitly assumed that all vehicles start and end at the same depot
    coords = helper.parse_instance(instance)

    # remove depot from list
    coords = coords[1:, :]

    # For this example, we implement a function that returns a random route. It is your task to come up
    # with a better approach to reduce the total distance covered, and provide a feasible solution
    n_customers = coords.shape[0]  # Number of customers

    # Generate a list of all customer indices
    customer_indices = list(range(1, n_customers + 1))  # Starting from 1 to n_customers

    # Shuffle the customer indices to randomize the route
    random.shuffle(customer_indices)

    # Generate the random routes, you should come up with something better...
    random_routes = helper.generate_random_routes(customer_indices)

    # Create the solution dictionary
    solution = {'routes': random_routes}
    print('\nRandom sequence solution (likely infeasible):')
    print(solution)

    # you should implement logic to generate the solution, it is not enough to just provide the solution sequence
    # NOTE: please remove all loading, writing, and print statements from your submission code

    return solution  # you need to return a solution in this exact (vrplib) format

# please keep the below code as-is, you can change the default "instance_path" to your liking. We provide example
# instances in the "Instances" folder, you can find more instances and their best-know-solution (BKS)
# at https://github.com/PyVRP/Instances

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run code.")
    parser.add_argument("--instance_path", default='Instances/X-n106-k14.vrp', type=str,
                        help="Path to a specific instance")

    args = parser.parse_args()

    # Read VRPLIB formatted instances
    instance = vrplib.read_instance(args.instance_path)
    sol = main(instance)

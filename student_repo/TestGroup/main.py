import numpy as np
import scipy
import pandas as pd
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
        instance : instance
    Returns:
        solution: solution in vrplib format.
    """

    print('\nPlease change the folder name "TestGroup" into your own group name, e.g., "Group1", '
          'this way we identify you in the competition, note that we only accept the naming convention "GroupX",'
          'other names are rejected by the system\n')

    # parse the instance into a dictionary
    instance_dict = helper.parse_instance(instance)

    # For this example, we implement a function that returns a random route, always starting from the same depot.
    # It is your task to come up with a better approach to reduce the total distance covered,
    # and provide a feasible solution
    depot_id = 1
    random_routes = helper.generate_random_routes_from_instance(instance_dict, depot_id)

    # Create the solution dictionary
    solution = {'routes': random_routes}
    print('\nRandom sequence solution (likely infeasible):')
    print(solution)

    # check feasibility of solution
    helper.check_solution_feasibility(solution, instance_dict)

    # find costs of solution
    profit = helper.total_profit_with_penalties(solution, instance_dict)
    print(f'profit: {profit}')

    # you should implement logic to generate the solution, it is not enough to just provide the solution sequence!
    # on the competition server, we will test your solution code on different (secret) instances that are of similar
    # size as the 3 instances provided. The computation time limit is 15 minutes in total for solving all 3 instances.

    print("RESULT:", solution)  # you need to return a solution in this exact (vrplib) format, do not change this!


# please keep the below code as-is, you can only change the default "instance_path" to your liking. We provide example
# instances in the "Instances" folder

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run code.")
    parser.add_argument("--instance_path", default='Instances/lrc53A.txt', type=str,
                        help="Path to a specific instance")

    args = parser.parse_args()

    # Read formatted instances
    instance = helper.read_instance(args.instance_path)
    sol = main(instance)

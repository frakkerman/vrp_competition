import vrplib
import numpy as np
import scipy
import pandas as pd
import os
import sys
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

    # Example using imported module Helper
    helper.test()

    # For this example, we directly return a solution read from a file
    # students should implement logic to generate the solution, so it is not enough to just provide the solution file
    # NOTE: please remove all loading, writing, and print statements from your submission code, i.e., remove the
    # line below, since it will yield an error on the submission platform since the provided path is not recognized
    solution = vrplib.read_solution("../Instances/Test/Sol/X-n101-k25.sol")
    # Example operation on the solution
    print(solution.keys())

    # see vrplib documentation for some reading and writing tools

    return solution # you need to return a solution in vrplib format

# NOTE: comment out all the below lines before submission, this code is only useful for locally running your code,
# but will yield errors when submitting


if __name__ == "__main__":
    # Read VRPLIB formatted instances, here you can read any instance you want locally
    instance = vrplib.read_instance("../../Instances/Test/X-n101-k25.vrp")
    sol = main(instance)

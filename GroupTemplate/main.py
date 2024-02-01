import vrplib
import numpy as np
import scipy
import pandas as pd

# These are the libraries we provide by default. If you want to use different Python libraries:
# please let us know so that we can add those to the competition environment.
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

    # For this example, we directly return a solution read from a file
    # In real scenarios, students should implement logic to generate the solution
    solution = vrplib.read_solution("../Instances/Test/Sol/X-n101-k25.sol")

    # see vrplib documentation for some reading and writing tools

    return solution


if __name__ == "__main__":
    # Read VRPLIB formatted instances, here you can read any instance you want
    instance = vrplib.read_instance("../Instances/Test/X-n101-k25.vrp")
    sol = main(instance)

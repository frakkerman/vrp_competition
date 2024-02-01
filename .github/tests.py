import os
import subprocess
import sys


def run_test_for_group(group_dir, instances_dir='../Instances/Test'):
    """
    Run the specified group's main.py against all instances in the instances directory.

    Parameters:
    - group_dir (str): The directory of the group, e.g., 'Groups/Group1'.
    - instances_dir (str): The directory where instance files are located.
    """
    # Ensure the specified directories exist
    if not os.path.isdir(group_dir):
        print(f"Error: Group directory '{group_dir}' does not exist.")
        return
    if not os.path.isdir(instances_dir):
        print(f"Error: Instances directory '{instances_dir}' does not exist.")
        return

    # Iterate over each instance file and run the group's main.py with it
    for instance_file in os.listdir(instances_dir):
        instance_path = os.path.join(instances_dir, instance_file)
        main_script_path = os.path.join(group_dir, 'main.py')
        print(f"Testing {group_dir} with instance {instance_file}...")
        result = subprocess.run(['python', main_script_path, instance_path], capture_output=True, text=True)

        # Print the stdout and stderr from running main.py
        print("Output:", result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        else:
            print("No errors")

if __name__ == "__main__":
    #The script expects the full path to the group's directory as the first command-line argument
    if len(sys.argv) < 2:
        print("Usage: python run_tests.py <FullPathToGroupDir>")
        sys.exit(1)

    group_dir = sys.argv[1]  # Full path to the group's directory is expected
    run_test_for_group(group_dir)

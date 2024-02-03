import os
import sys
import importlib.util
import vrplib
import time
import json
import numpy as np
import re
from datetime import datetime


def read_leaderboard(readme_path):
    """Read the existing leaderboard from README."""
    with open(readme_path, 'r', encoding='utf-8') as file:
        content = file.read()

    leaderboard_content = re.search('<!-- LEADERBOARD_START -->(.*?)<!-- LEADERBOARD_END -->', content, re.DOTALL)
    if leaderboard_content:
        return leaderboard_content.group(1).strip(), content
    return "", content


def get_score(entry):
    try:
        return float(entry['Score'])
    except ValueError:
        return float('inf')


def update_leaderboard(readme_path, new_entry):
    """Update the leaderboard with a new entry, formatting as a Markdown table."""
    leaderboard, full_content = read_leaderboard(readme_path)
    entries = []

    # Parse the existing leaderboard table into a list of dictionaries
    if leaderboard:
        lines = leaderboard.strip().split('\n')
        headers = [header.strip() for header in lines[0].strip('|').split('|')]
        for line in lines[1:]:
            values = [value.strip() for value in line.strip('|').split('|')]
            entry = dict(zip(headers, values))
            entries.append(entry)

    # Get the date for the new entry
    today = datetime.now().strftime("%Y-%m-%d")
    new_entry['Date'] = today

    # Check if the group already exists in the leaderboard
    group_number = new_entry['GroupNumber']
    existing_entry = None
    for entry in entries:
        if entry['GroupNumber'] == group_number:
            existing_entry = entry
            break

    # If the group already exists, update it only if the new entry has a better score
    if existing_entry:
        existing_score = float(existing_entry['Score'])
        new_score = float(new_entry['Score'])
        if new_score < existing_score:
            existing_entry.update(new_entry)
        # do not allow 2 submissions on same day, so make all entries invalid
        if existing_entry['Date'] == new_entry['Date']:
            existing_entry['Passed'] = '❌'
    else:
        # Append new entry as a dictionary if the group is not in the leaderboard
        entries.append(new_entry)

    # Separate entries into two lists: passed_entries and failed_entries
    passed_entries = []
    failed_entries = []

    for i in range(1, len(entries)):
        entry = entries[i]
        if entry['Passed'] == '✅':
            passed_entries.append(entry)
        else:
            failed_entries.append(entry)

    # Sort passed_entries by Score
    passed_entries.sort(key=lambda x: x['Score'])

    # Combine the sorted passed_entries with failed_entries
    entries = passed_entries + failed_entries

    for rank, entry in enumerate(entries, start=1):  # Start from the second entry
        entry['Rank'] = rank

    # Prepare the Markdown table headers and rows
    table_headers = "| Rank | Date | GroupNumber | Passed | Score | Runtime |\n| ------ | ------------ | ------------------- |-------------| ------- | ------- |"
    table_rows = [f"| {entry['Rank']} | {entry['Date']} | {entry['GroupNumber']} | {entry['Passed']} | {entry['Score']} | {entry['Runtime']} |" for entry in entries]
    new_leaderboard_content = table_headers + '\n' + '\n'.join(table_rows)

    # Replace old leaderboard content in the full README content
    updated_content = re.sub(r'<!-- LEADERBOARD_START -->(.*?)<!-- LEADERBOARD_END -->',
                             f'<!-- LEADERBOARD_START -->\n{new_leaderboard_content}\n<!-- LEADERBOARD_END -->',
                             full_content, flags=re.DOTALL)

    # Write updated content back to README
    with open(readme_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)
    print('Finished, results (if applicable) written to leaderboard')


def parse_solution(solution_dict):
    """Extracts routes from the solution dictionary."""
    # Directly access the 'routes' key from the dictionary
    routes = solution_dict['routes']
    return routes


def parse_instance(instance_dict):
    """Parse the instance dictionary to extract node coordinates."""
    node_coords = np.array(instance_dict['node_coord'])
    return node_coords


def calculate_euclidean_distance(coord1, coord2):
    """Calculate the Euclidean distance between two points."""
    return np.linalg.norm(np.array(coord1) - np.array(coord2))


def calculate_total_distance(routes, node_coords):
    """Calculate the total Euclidean distance for the given routes based on node coordinates.
    Assumes the first entry in node_coords is the depot and all routes start and end at the depot.
    """
    total_distance = 0
    depot_coord = node_coords[0]  # Coordinates of the depot
    for route in routes:
        if not route:  # Skip empty routes
            continue
        # Distance from depot to the first node
        total_distance += calculate_euclidean_distance(depot_coord, node_coords[route[0] - 1])
        for i in range(len(route) - 1):
            coord1 = node_coords[route[i] - 1]
            coord2 = node_coords[route[i + 1] - 1]
            total_distance += calculate_euclidean_distance(coord1, coord2)
        # Distance from the last node back to the depot
        total_distance += calculate_euclidean_distance(node_coords[route[-1] - 1], depot_coord)
    return total_distance


def normalize_score(value, max_value):
    """
    Normalize a value to a 0-1 scale, where 0 represents the maximum value
    and 1 represents 0 in the original scale, indicating better performance.
    """
    return 1 - (value / max_value)


def calculate_weighted_score(distance, runtime, max_distance, max_runtime):
    """
    Calculate a weighted score with 90% weight for distance and 10% for runtime.
    """
    # Normalize distance and runtime
    normalized_distance_score = 100*normalize_score(distance, max_distance)
    normalized_runtime_score = 100*normalize_score(runtime, max_runtime)

    # Apply weights
    weighted_score = (0.9 * normalized_distance_score) + (0.1 * normalized_runtime_score)

    return weighted_score



def run_test_for_group(group_dir, instances_dir='Instances/Test'):  # local debug: '../Instances/Test'
    """
    Run the specified group's main.py against all instances in the instances directory.

    Parameters:
    - group_dir (str): The directory of the group, e.g., 'Groups/TestGroup'.
    - instances_dir (str): The directory where instance files are located.
    """
    # Ensure the specified directories exist
    if not os.path.isdir(group_dir):
        print(f"Error: Group directory '{group_dir}' does not exist.")
        return
    if not os.path.isdir(instances_dir):
        print(f"Error: Instances directory '{instances_dir}' does not exist.")
        return

    # Construct the path to the group's main.py
    main_py_path = os.path.join(group_dir, 'main.py')

    # Dynamically import the group's main.py
    spec = importlib.util.spec_from_file_location("module.name", main_py_path)
    group_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(group_module)

    instance_path = 'Instances/Test/X-n101-k25.vrp'  # for GitHub
    #instance_path = '../Instances/Test/X-n101-k25.vrp'  # local debug

    test_passed = False

    print(f"Testing {group_dir} with instance {instance_path}...")
    # Read the instance using vrplib
    instance = vrplib.read_instance(instance_path)
    # Execute the main function

    time_limit = 300  # Replace with your desired time limit

    start_time = time.time()
    try:
        # Run the test
        solution = group_module.main(instance)

        # Check if the elapsed time exceeds the time limit
        elapsed_time = time.time() - start_time
        if elapsed_time > time_limit:
            raise TimeoutError(f"Test exceeded the time limit of {time_limit} seconds")

        test_passed = True
    except TimeoutError as te:
        print(f"Test failed due to timeout: {te}")
    except Exception as e:
        print(f"Test failed: {e}")

    end_time = time.time()
    runtime = end_time - start_time

    # Parsing the solution and instance
    solution_routes = parse_solution(solution)
    node_coords = parse_instance(instance)

    # Calculate the total distance
    total_distance = calculate_total_distance(solution_routes, node_coords)
    print(f"Total Euclidean distance of the solution: {total_distance}")

    max_distance = 100000  # Maximum expected distance
    max_runtime = 300  # Maximum expected runtime in seconds
    score = calculate_weighted_score(total_distance, runtime, max_distance, max_runtime)

    # Output test result information
    output = {
        "GroupNumber": group_dir.split('/')[-1],  # Example group number
        "Passed": '✅' if test_passed else '❌',
        "Score": str(score),
        "Runtime": f"{runtime:.2f}s"
    }
    print(json.dumps(output))

    readme_path = '../README.md'

    update_leaderboard(readme_path, output)

if __name__ == "__main__":
    # The script expects the full path to the group's directory as the first command-line argument
    if len(sys.argv) < 2:
        print("Usage: python run_tests.py <FullPathToGroupDir>")
        sys.exit(1)

    group_dir = sys.argv[1]  # Full path to the group's directory is expected

    #group_dir = '../Groups/TestGroup' # For local debug, comment on GitHub
    run_test_for_group(group_dir)

import re
import pandas as pd
import subprocess
import argparse
import os
import pathlib


def run_command(command):
    """Run a command in the shell and return its output."""
    result = subprocess.run(
        command, shell=False, capture_output=True, text=True
    )
    if result.returncode != 0:
        raise Exception(f"Error running command '{command}': {result.stderr}")
    return result.stdout

def list_assignments_from_classroom(classroom_id):
    data = run_command(
        ["gh", "classroom", "assignments", "-c", str(classroom_id)]
    )

    df = get_df_from(data, 2)

    return df


def clone_assignment_submissions_to_folder(assignment_id, folder):
    data = run_command(
        [
            "gh",
            "classroom",
            "clone",
            "student-repos",
            "-a",
            str(assignment_id),
            "-d",
            folder,
        ]
    )
    return data


def view_classroom_info(classroom_id):
    return run_command(["gh", "classroom", "view", "-c", str(classroom_id)])


def view_assignment_info(assignment_id):
    return run_command(
        ["gh", "classroom", "assignment", "-a", str(assignment_id)]
    )


def clone_all_assignments_from_classroom_to_folder(classroom_id, folder):
    print(view_classroom_info(classroom_id))
    df = list_assignments_from_classroom(classroom_id)
    assignment_ids = list(df.iloc[:, 0])
    
    print(assignment_ids)

   
    print(view_assignment_info(582369))
        
    print(clone_assignment_submissions_to_folder(582369, folder))


def parse_assignment_info(assignment_id):
    data = str(view_assignment_info(assignment_id))

    clean_data = clean_data = re.sub(r"\x1b\[[0-9;]*m", "", data)

    # Split the output into lines
    lines = clean_data.strip().split("\n")

    # Filter out empty lines and section titles
    lines = [
        line
        for line in lines
        if line
        and not line.startswith("CLASSROOM INFORMATION")
        and not line.startswith("ASSIGNMENT INFORMATION")
    ]

    # Extract information as key-value pairs
    clean_data = {}
    for line in lines:
        key, value = line.split(":", 1)
        clean_data[key.strip()] = value.strip()

    # Create a DataFrame
    df = pd.DataFrame([clean_data])

    # Display the DataFrame
    return df


def get_all_assignments_info_from_classroom(classroom_id):
    df = list_assignments_from_classroom(classroom_id)

    assignment_ids = list(df.iloc[:, 0])

    lines = []
    for a in assignment_ids:
        lines.append(parse_assignment_info(a))

    df_assignments = pd.concat(lines)

    return df_assignments.set_index("ID")


def df_accepted_from_assignment(assignment_id):
    data = run_command(
        ["gh", "classroom", "accepted-assignments", "-a", str(assignment_id)]
    )
    return get_df_from(data, headers_pos=3)


def df_all_accepted_assignments_from_classroom(classroom_id):
    df = list_assignments_from_classroom(classroom_id)

    assignment_ids = list(df.iloc[:, 0])

    lines = []
    for a in assignment_ids[:]:
        df_accepted = df_accepted_from_assignment(a)
        df_accepted["ID_AS"] = a
        lines.append(df_accepted.set_index(["ID_AS", "Student"]).sort_index())

    if lines:
        df_assignments = pd.concat(lines, axis=0)

    return df_assignments

def get_df_from(data, headers_pos):
    # Remove ANSI escape codes for coloring
    clean_data = re.sub(r"\x1b\[[0-9;]*m", "", data)

    # Split the string into lines
    lines = clean_data.split("\n")

    # Extract headers
    headers = lines[headers_pos].split("\t")

    # Extract the data rows
    rows = [line.split("\t") for line in lines[headers_pos + 1 : -1]]

    # Create DataFrame
    df = pd.DataFrame(rows, columns=headers)

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clone student repos.")
    parser.add_argument("--classroom_id", default=12345, type=int, help="The GitHub Classroom ID")
    parser.add_argument("--repos_dir", default='home_path/repos/', type=str,help="Directory to clone the repositories into")
    args = parser.parse_args()

    if args.classroom_id and args.repos_dir:
        
        clone_all_assignments_from_classroom_to_folder(
            args.classroom_id, args.repos_dir
        )
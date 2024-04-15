import os
import pathlib
import subprocess
import argparse
import re
import helper
import ast
import csv
import time
from datetime import datetime

def calculate_score(cumulative_profits, total_runtime_seconds, max_profit=225000, max_runtime_seconds=1800):
    normalized_profit = cumulative_profits / max_profit
    normalized_runtime = 1 - (total_runtime_seconds / max_runtime_seconds)
    score = (normalized_profit * 0.6) + (normalized_runtime * 0.4)
    return score


def run_in_repo(repo_path, original_dir, instances):
    group_folder_pattern = re.compile(r'^Group\d+$')
    group_folder_path = None
    instance_results = []

    for item in os.listdir(repo_path):
        if group_folder_pattern.match(item) and os.path.isdir(os.path.join(repo_path, item)):
            group_folder_path = os.path.join(repo_path, item)
            break

    if not group_folder_path:
        print(f"No group folder found in {repo_path}. Skipping...")
        return

    os.chdir(group_folder_path)
    group_name = os.path.basename(group_folder_path)
    
    for instance in instances:
        error_message, feasibility_checks = "", []
        start_time = time.time()

        try:
            result = subprocess.run(['python3', 'main.py', '--instance_path', instance], capture_output=True, text=True, check=True, timeout=605)
            runtime = time.time() - start_time
            
            output_lines = result.stdout.strip().split('\n')
            output_line = next((line for line in output_lines if line.startswith("RESULT:")), None)
            
            if output_line:
                dict_str = output_line.replace("RESULT: ", "").strip()
                try:
                    result_dict = ast.literal_eval(dict_str)
                    read_instance = helper.read_instance(instance)
                    instance_dict = helper.parse_instance(read_instance)

                    # Proceed with feasibility checks and cost calculation
                    feasible = True
                    if not helper.check_vehicle_capacity(result_dict, instance_dict, instance_dict.get('vehicle_capacity', 0)):
                        feasibility_checks.append("Vehicle capacity exceeded")
                        feasible = False
                    if not helper.check_start_end_at_depot(result_dict, instance_dict):
                        feasibility_checks.append("Route does not start/end at depot")
                        feasible = False
                    if not helper.check_number_of_trucks(result_dict, instance_dict.get('number_of_trucks', 0)):
                        feasibility_checks.append("Number of trucks exceeded")
                        feasible = False
                    if not helper.check_pickup_before_delivery(result_dict, instance_dict):
                        feasibility_checks.append("Delivery before pickup OR only pickup, no delivery")
                        feasible = False
                    if not helper.check_no_duplicate_visits(result_dict):
                        feasibility_checks.append("Visiting customer(s) more than once")
                        feasible = False
                    
                    profit = helper.total_profit_with_penalties(result_dict, instance_dict)# if feasible else '-inf'
                    feasibility = "Yes" if feasible else "No"
                except Exception as e:
                    error_message = str(e)
                    feasibility = "No"
                    profit = '-inf'
            else:
                feasibility = "No"
                profit = '-inf'
                error_message = "No RESULT line found"
                
            instance_results.append((os.path.basename(instance), f"{runtime:.2f}", feasibility, profit, "; ".join([f"[{msg}]" for msg in feasibility_checks]) if feasibility_checks else f"[{error_message}]"))

        except subprocess.TimeoutExpired as e:
            runtime = (time.time() - start_time)
            error_details = e.stderr if e.stderr else "No error details available."
            # Include both the default error message and the specific error details
            error_message = f"[Error running script: {e}. Details: {error_details}]"
            instance_results.append((os.path.basename(instance), f"{runtime:.2f}", "No", '-inf', error_message))

        except subprocess.CalledProcessError as e:
            runtime = (time.time() - start_time)
            error_details = e.stderr if e.stderr else "No error details available."
            # Include both the default error message and the specific error details
            error_message = f"[Error running script: {e}. Details: {error_details}]"
            instance_results.append((os.path.basename(instance), f"{runtime:.2f}", "No", '-inf', error_message))

            #runtime = time.time() - start_time
            #error_message = str(e)
            #instance_results.append((os.path.basename(instance), f"{runtime:.2f}", "No", '-inf', f"[Error running script: {error_message}]"))

    # Write group-specific CSV
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
    csv_file_path = os.path.join(original_dir, "run_output", f"{group_name}_{current_datetime}.csv")
    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Instance", "Runtime (seconds)", "Feasible", "Profit", "Error"])
        for result in instance_results:
            writer.writerow(result)

    # Append to central results CSV
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    central_results_file_path = os.path.join(original_dir, "run_output", "central_results.csv")
    with open(central_results_file_path, mode='a', newline='') as central_file:
        central_writer = csv.writer(central_file)
        # If this is the first entry, write the header with an additional "Date Time" column
        if central_file.tell() == 0:
            central_writer.writerow(["Group", "Cumulative Profits", "Total Runtime (seconds)", "Overall Feasible", "Score", "Date Time"])
        # Convert total runtime to minutes for score calculation
        total_runtime = sum(float(runtime) for _, runtime, _, _, _ in instance_results)
        overall_feasible = "Yes" if all(fea == "Yes" for _, _, fea, _, _ in instance_results) else "No"
        total_runtime_minutes = total_runtime / 60
        
        # Ensure cumulative profits and runtime are in the correct format and calculate the score
        if overall_feasible == "Yes":
            cumulative_profits = sum(float(profit) for _, _, _, profit, _ in instance_results if profit != '-inf')
            score = calculate_score(cumulative_profits, total_runtime_minutes)
        else:
            score = "N/A"  # or set to a default value indicating infeasibility
            cumulative_profits = sum(float(profit) for _, _, _, profit, _ in instance_results if profit != '-inf')
        # Then append the calculated score to your central_writer.writerow call
        central_writer.writerow([group_name, f"{cumulative_profits:.2f}", f"{total_runtime:.2f}", overall_feasible, score, current_datetime])
    
        os.chdir(original_dir)

def process_assignments_in_folder(root_folder, instances_folder):
    # List all instance paths in the specified folder
    instance_paths = [str(pathlib.Path(instances_folder) / f) for f in os.listdir(instances_folder) if os.path.isfile(os.path.join(instances_folder, f))]
    
    for assignment_folder in os.listdir(root_folder):
        a_folder = os.path.join(root_folder, assignment_folder)

        if not os.path.isdir(a_folder):
            continue

        print("#### ASSIGNMENT repo name:", assignment_folder)

        for repo in os.listdir(a_folder):
            dir_repo = pathlib.Path(root_folder) / assignment_folder / repo

            if os.path.isdir(dir_repo):
                print("Processing repo:", dir_repo)
                run_in_repo(dir_repo, root_folder, instance_paths)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process assignments with multiple instances in specific group folders.")
    parser.add_argument("--repos_dir", default='home_path/repos/', type=str, help="Directory with the repositories")
    parser.add_argument("--instances_folder", default='home_path/competition_master/Instances/', type=str, help="Folder containing instance files")

    args = parser.parse_args()

    if args.repos_dir:
        os.makedirs(args.repos_dir, exist_ok=True)
        process_assignments_in_folder(args.repos_dir, args.instances_folder)

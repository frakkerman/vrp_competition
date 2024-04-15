import subprocess
import argparse
import os
import pathlib
import shutil

def run_command(command):
    """Run a command in the shell and return its output."""
    result = subprocess.run(
        command, shell=False, capture_output=True, text=True
    )
    if result.returncode != 0:
        error_msg = f"Error running command '{' '.join(command)}': {result.stderr}"
        print(f"STDOUT: {result.stdout}")  # Print stdout for additional context
        raise Exception(error_msg)
    return result.stdout


def git_add_commit_push(repo_path, folder_containing_csvs, commit_message="Update CSV files"):
    os.chdir(repo_path)
    
     # Optionally stash any unstaged changes
    run_command(["git", "stash", "push", "-m", "Temporary stash before pull"])

    # Pull the latest changes from the remote repository to avoid conflicts
    run_command(["git", "pull", "--rebase"])

    # Check if there are any stash entries before trying to pop
    stash_list = run_command(["git", "stash", "list"])
    if stash_list.strip():  # If there are stash entries
        run_command(["git", "stash", "pop"])
    
    target_folder_in_repo = 'output'

    # Copy CSV files to the target folder within the repo
    target_folder_path = os.path.join(repo_path, target_folder_in_repo)
    os.makedirs(target_folder_path, exist_ok=True)  # Ensure target folder exists

    for file in os.listdir(folder_containing_csvs):
        if file.endswith(".csv"):
            source_file_path = os.path.join(folder_containing_csvs, file)
            destination_file_path = os.path.join(target_folder_path, file)
            shutil.copy2(source_file_path, destination_file_path)  # Copy file to target folder

    # Stage all changes in the repository, including new, modified, and deleted files
    run_command(["git", "add", "."])

    # Check if there are changes to commit
    status_result = run_command(["git", "status", "--porcelain"])
    if status_result.strip():  # If this is not empty, there are changes
        # Committing changes
        run_command(["git", "commit", "-m", commit_message])
        # Pushing changes
        run_command(["git", "push"])
        print("Changes have been committed and pushed to GitHub.")
    else:
        print("No changes to commit.")





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Push CSV files to GitHub repo.")
    parser.add_argument("--repo_path", default = 'home_path/vrp_competition_leaderboard/', type=str, help="Path to the local git repository.")
    parser.add_argument("--folder_containing_csvs",default='home_path/repos/run_output/', type=str, help="Folder containing CSV files to push.")
    parser.add_argument("--commit_message", default="Update CSV files", type=str, help="Commit message for the changes.")

    args = parser.parse_args()

    # Ensure both the repository path and the folder path are provided
    if args.repo_path and args.folder_containing_csvs:
        # Ensure paths are absolute
        repo_path = os.path.abspath(args.repo_path)
        folder_containing_csvs = os.path.abspath(args.folder_containing_csvs)
        
        # Run the git commands to add, commit, and push the CSV files
        git_add_commit_push(repo_path, folder_containing_csvs, args.commit_message)

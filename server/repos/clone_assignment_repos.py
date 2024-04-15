import pandas as pd
import os
import subprocess

import shutil

def delete_folder_contents(folder_path):
    # Check if the specified path is an existing directory
    if not os.path.isdir(folder_path):
        print(f"The path {folder_path} does not exist or is not a directory.")
        return
    
    # Loop through each item in the folder
    for item_name in os.listdir(folder_path):
        # Create the full path to the item
        item_path = os.path.join(folder_path, item_name)
        
        # Check if this item is a file or a directory
        if os.path.isfile(item_path) or os.path.islink(item_path):
            # If it's a file or a symlink, delete it
            os.remove(item_path)
        elif os.path.isdir(item_path):
            # If it's a directory, delete it and all its contents
            shutil.rmtree(item_path)
    
    print(f"All contents of the folder {folder_path} have been deleted.")

# Save CSV data to a file (for this example, we'll directly read it from a string)
csv_file_path = 'home_path/repos/github_classroom_id.csv'

# Load the CSV data into a pandas DataFrame
df = pd.read_csv(csv_file_path)

# Create a folder where all repositories will be cloned
clone_folder = 'home_path/repos/assignment_folder/'

delete_folder_contents(clone_folder)

os.makedirs(clone_folder, exist_ok=True)

# Iterate through the DataFrame and clone each repository
for index, row in df.iterrows():
    # Original HTTPS URL from the CSV
    https_repo_url = row['student_repository_url']
    
    # Convert HTTPS URL to SSH URL
    repo_url = https_repo_url.replace("https://github.com/", "git@github.com:")
    
    clone_path = os.path.join(clone_folder, row['student_repository_name'])
    #if not os.path.exists(clone_path):
    print(f"Cloning repository: {repo_url}")
    subprocess.run(['git', 'clone', repo_url, clone_path])
    #else:
     #   print(f"Repository already cloned: {repo_url}")


print("Cloning complete.")

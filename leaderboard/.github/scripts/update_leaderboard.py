import pandas as pd
import numpy as np

# Load the CSV file
df = pd.read_csv('output/central_results.csv')

# Convert "Date Time" to datetime for sorting
df['Date Time'] = pd.to_datetime(df['Date Time'])

# Process the DataFrame
# 1. Prioritize feasible solutions
# 2. Sort by score (descending, since higher is better), then by Date Time (most recent first)
# 3. Drop duplicates, keeping the first occurrence (best score per group)
best_scores = df.sort_values(by=['Overall Feasible', 'Score', 'Date Time'], ascending=[False, False, False])\
                .drop_duplicates('Group')

# Read the existing README.md content
with open('README.md', 'r') as file:
    content = file.read()

# Find the leaderboard section and prepare new content
start = content.find('<!-- LEADERBOARD_START -->') + len('<!-- LEADERBOARD_START -->')
end = content.find('<!-- LEADERBOARD_END -->')
leaderboard_header = "| Rank | Date | GroupNumber | Feasible/Bugs | Score | Cumulative profit | Runtime |\n| ------ | ------------ | ------------------- |-------------| ------- | ------- | ------- |"

new_leaderboard_rows = []
rank = 1
for i, row in best_scores.iterrows():
    passed_icon = '✅' if row['Overall Feasible'] == 'Yes' else '❌'
    date_str = row['Date Time'].strftime("%Y-%m-%d %H:%M")
    new_leaderboard_rows.append(f"| {rank} | {date_str} | {row['Group']} | {passed_icon} | {np.round(100.0*row['Score'],2)} | {np.round(row['Cumulative Profits'],2)} | {row['Total Runtime (seconds)']}s |")
    rank += 1

new_leaderboard_content = "\n".join([leaderboard_header] + new_leaderboard_rows)

# Replace the old leaderboard section with the new content
new_content = content[:start] + "\n" + new_leaderboard_content + "\n" + content[end:]

# Write the updated content back to README.md
with open('README.md', 'w') as file:
    file.write(new_content)

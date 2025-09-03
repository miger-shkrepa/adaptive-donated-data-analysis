import os
import csv

# Variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Prepare the CSV file path
csv_file_path = 'query_responses/results.csv'

# Ensure the directory for the CSV file exists
os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

# Write the CSV file with only the column headers
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Account'])

print(f"CSV file with column headers created at {csv_file_path}")
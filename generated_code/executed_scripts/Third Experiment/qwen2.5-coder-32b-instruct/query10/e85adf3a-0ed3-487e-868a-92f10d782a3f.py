import os
import csv

# The variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Since there is no data indicating content views or accounts, we create a CSV with only headers
output_file_path = 'query_responses/results.csv'

# Ensure the directory exists
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

# Write the CSV file with headers
with open(output_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Account', 'Post Views', 'Video Views'])

print(f"CSV file with headers created at {output_file_path}")
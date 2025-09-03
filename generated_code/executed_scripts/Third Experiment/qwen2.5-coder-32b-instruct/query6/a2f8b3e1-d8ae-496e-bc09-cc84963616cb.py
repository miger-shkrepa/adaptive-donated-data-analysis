import os
import csv
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Since the necessary files for account changes are not available, we create an empty CSV with headers
output_file_path = 'query_responses/results.csv'

# Ensure the directory exists
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

# Write the CSV file with only the column headers
with open(output_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Changed', 'New Value', 'Change Date'])

print(f"CSV file created at {output_file_path} with only column headers.")
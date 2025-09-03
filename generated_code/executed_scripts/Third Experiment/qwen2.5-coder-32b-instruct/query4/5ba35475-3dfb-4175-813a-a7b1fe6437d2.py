import os
import csv

# Variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Define the path for the output CSV file
output_csv_path = 'query_responses/results.csv'

# Ensure the directory for the output file exists
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

# Write the CSV file with only the column headers
with open(output_csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Company Name'])

print(f"CSV file with column headers has been created at {output_csv_path}")
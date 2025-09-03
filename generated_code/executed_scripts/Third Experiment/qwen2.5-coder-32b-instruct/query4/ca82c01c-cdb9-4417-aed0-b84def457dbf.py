import os
import csv

# The variable referring to the file input must be declared in a single line.
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Define the path for the output CSV file
output_csv_path = 'query_responses/results.csv'

# Ensure the directory for the output file exists
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

# Open the CSV file and write the header
with open(output_csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Company Name'])

# Since there is no data about companies accessing Instagram activity or information,
# the CSV file will only contain the header.
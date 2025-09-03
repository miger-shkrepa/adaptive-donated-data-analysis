import os
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Define the output file path
output_file_path = 'query_responses/results.csv'

# Create the directory for the output file if it does not exist
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

# Open the CSV file and write the header
with open(output_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Device ID', 'Login Time'])

# Since the necessary data is not available, the CSV will only contain the headers.
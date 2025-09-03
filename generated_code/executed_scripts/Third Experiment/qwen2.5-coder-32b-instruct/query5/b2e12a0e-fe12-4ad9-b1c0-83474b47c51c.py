import os
import csv
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

def generate_login_csv(root_dir):
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    # Since the required data is not present in the provided structure,
    # we will create a CSV file with only the column headers.
    csv_file_path = 'query_responses/results.csv'
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    
    # Write the CSV file with only the column headers
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Device ID', 'Login Time'])

# Call the function to generate the CSV
generate_login_csv(root_dir)
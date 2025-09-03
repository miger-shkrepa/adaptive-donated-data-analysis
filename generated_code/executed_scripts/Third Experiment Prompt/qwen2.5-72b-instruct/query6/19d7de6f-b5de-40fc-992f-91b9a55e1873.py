import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Create the output directory if it doesn't exist
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

def process_directory(root):
    try:
        # Check if the root directory exists
        if not os.path.exists(root):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize the CSV file with headers
        with open(output_csv, 'w', newline='') as csvfile:
            fieldnames = ['Changed', 'New Value', 'Change Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

        # Since there are no specific files for account changes, return the CSV with headers only
        print(f"CSV file created at {output_csv} with headers only.")

    except Exception as e:
        print(f"Error: {e}")

# Execute the function with the root directory
process_directory(root_dir)
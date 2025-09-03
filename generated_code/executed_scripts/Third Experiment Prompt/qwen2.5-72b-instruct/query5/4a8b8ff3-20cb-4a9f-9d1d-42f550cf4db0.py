import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def process_data(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        output_file = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ['Device ID', 'Login Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # Since the directory structure does not contain login information,
            # we will not write any rows to the CSV file.
            
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

if __name__ == "__main__":
    process_data(root_dir)
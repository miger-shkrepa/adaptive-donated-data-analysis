import os
import csv
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Prepare the CSV file path
csv_file_path = 'query_responses/results.csv'

# Create the directory if it does not exist
os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

# Open the CSV file and write the header
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Changed', 'New Value', 'Change Date'])

# Since there is no data available, the CSV will only contain the headers
import os
import csv

# The root directory variable
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Define the path for the output CSV file
output_csv_path = 'query_responses/results.csv'

# Create the directory for the output CSV file if it does not exist
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

# Open the CSV file and write the header
with open(output_csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['User', 'Times Engaged'])

# Since the necessary data for stories is not available, we only write the header
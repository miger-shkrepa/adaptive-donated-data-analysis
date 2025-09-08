import os
import csv

root_dir = "root_dir"

# Check if the root directory exists
if not os.path.isdir(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Define the CSV file path
csv_file_path = "query_responses/results.csv"

# Define the CSV column headers
headers = ["Account", "Post Views", "Video Views"]

# Create the CSV file and write the headers
with open(csv_file_path, "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(headers)

print(f"CSV file created at: {csv_file_path}")
import csv
import os

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

output_file = "query_responses/results.csv"

with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['Company Name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
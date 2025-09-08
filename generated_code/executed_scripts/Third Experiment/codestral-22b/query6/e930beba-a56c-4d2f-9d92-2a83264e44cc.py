import os
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

output_file = "query_responses/results.csv"

with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Changed", "New Value", "Change Date"])
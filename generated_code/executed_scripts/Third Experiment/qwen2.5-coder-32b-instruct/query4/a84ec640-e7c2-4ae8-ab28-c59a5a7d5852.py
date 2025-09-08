import os
import csv

# Variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Since there is no information about companies accessing Instagram activity or information,
# we will create an empty CSV file with the column header "Company Name".
output_file_path = 'query_responses/results.csv'

# Ensure the directory exists
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

# Write the CSV file with the header only
with open(output_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Company Name"])

print(f"CSV file created at {output_file_path} with the column header 'Company Name' and no data rows.")
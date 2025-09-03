import os
import csv

# Variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Since there is no data on engagement, we create a CSV with only the headers
output_path = 'query_responses/results.csv'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Writing the CSV file with only headers
with open(output_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['User', 'Times Engaged'])

print(f"CSV file created at {output_path} with only headers.")
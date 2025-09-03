import csv
import json
import os

# Define the root directory variable
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Define the input JSON file path
input_json = os.path.join(root_dir, 'personal_information', 'profile_changes.json')

# Check if the input JSON file exists
if not os.path.exists(input_json):
    print("Warning: The input JSON file does not exist. Returning CSV file with only column headers.")
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Changed', 'New Value', 'Change Date'])
    exit()

# Load the input JSON file
with open(input_json, 'r') as f:
    profile_changes = json.load(f)

# Initialize the output CSV file
with open(output_csv, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Changed', 'New Value', 'Change Date'])

# Iterate over the profile changes
for change in profile_changes:
    writer.writerow([change['changed'], change['new_value'], change['change_date']])

print("Query response saved to:", output_csv)
import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Define the output file path
output_file = "query_responses/results.csv"

# Define the input file path
input_file = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")

# Check if the input file exists
if not os.path.exists(input_file):
    # If the file does not exist, return a CSV file with only the column headers
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Changed", "New Value", "Change Date"])
    print("Warning: The input file does not exist. Returning a CSV file with only the column headers.")
    exit()

# Load the input file
try:
    with open(input_file, "r") as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    raise ValueError("ValueError: The input file is not a valid JSON file.") from e

# Initialize the output list
output = []

# Iterate over the profile changes
for change in data["profile_user"]:
    # Extract the changed field, new value, and change date
    changed = change["string_map_data"]["Name"]["value"]
    new_value = change["string_map_data"]["Email"]["value"]
    change_date = change["string_map_data"]["Date of birth"]["value"]

    # Append the output to the list
    output.append([changed, new_value, change_date])

# Write the output to the CSV file
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Changed", "New Value", "Change Date"])
    writer.writerows(output)

print("Query completed successfully.")
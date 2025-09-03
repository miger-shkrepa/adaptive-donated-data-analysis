import csv
import json
import os

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
    print("Error: The file {} does not exist.".format(input_file))
    exit()

# Load the input file
with open(input_file, "r") as f:
    data = json.load(f)

# Extract the profile changes data
profile_changes = data["profile_profile_change"]

# Initialize the output data
output_data = []

# Iterate over the profile changes
for change in profile_changes:
    # Extract the changed, new value, and change date
    changed = change["string_map_data"]["Changed"]["value"]
    new_value = change["string_map_data"]["New Value"]["value"]
    change_date = change["string_map_data"]["Change Date"]["value"]

    # Add the data to the output list
    output_data.append([changed, new_value, change_date])

# Write the output data to the CSV file
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Changed", "New Value", "Change Date"])
    writer.writerows(output_data)

print("Query completed successfully.")
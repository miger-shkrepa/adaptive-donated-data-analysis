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

# Extract the relevant data
changes = []
for change in data["profile_profile_change"]:
    changed = change["string_map_data"]["Changed"]["value"]
    new_value = change["string_map_data"]["New Value"]["value"]
    change_date = change["string_map_data"]["Change Date"]["value"]
    changes.append([changed, new_value, change_date])

# Write the results to the output file
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Changed", "New Value", "Change Date"])
    writer.writerows(changes)

print("Query results written to {}".format(output_file))
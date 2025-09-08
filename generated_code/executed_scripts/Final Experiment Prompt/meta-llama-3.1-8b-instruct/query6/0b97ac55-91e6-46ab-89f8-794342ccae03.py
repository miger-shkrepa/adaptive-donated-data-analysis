import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Define the file path to the profile changes JSON file
profile_changes_file = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")

# Check if the profile changes file exists
if not os.path.exists(profile_changes_file):
    # If the file does not exist, return a CSV file with only the column headers
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Changed", "New Value", "Change Date"])
    print("Warning: The profile changes file does not exist. Returning CSV with only column headers.")
    exit()

# Load the profile changes JSON file
try:
    with open(profile_changes_file, "r") as f:
        profile_changes_data = json.load(f)
except json.JSONDecodeError as e:
    raise ValueError("ValueError: Failed to parse JSON in profile changes file: " + str(e))

# Initialize an empty list to store the changes
changes = []

# Iterate over the profile changes data
for change in profile_changes_data:
    # Extract the changed field, new value, and change date
    changed_field = change.get("changed_field", "")
    new_value = change.get("new_value", "")
    change_date = change.get("change_date", "")

    # Check if the changed field, new value, and change date are not empty
    if changed_field and new_value and change_date:
        # Append the change to the list
        changes.append([changed_field, new_value, change_date])

# Write the changes to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Changed", "New Value", "Change Date"])
    writer.writerows(changes)

print("Query completed successfully.")
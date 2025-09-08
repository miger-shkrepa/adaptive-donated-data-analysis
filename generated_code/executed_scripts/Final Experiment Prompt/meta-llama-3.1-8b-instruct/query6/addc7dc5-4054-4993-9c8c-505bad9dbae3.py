import csv
import json
import os

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
    print("Error: The profile changes file does not exist.")
    exit()

# Load the profile changes JSON file
with open(profile_changes_file, "r") as f:
    profile_changes_data = json.load(f)

# Extract the profile changes data
profile_changes = profile_changes_data.get("profile_profile_change", [])

# Initialize an empty list to store the profile changes
profile_changes_list = []

# Iterate over the profile changes
for change in profile_changes:
    # Extract the changed, new value, and change date
    changed = change.get("string_map_data", {}).get("Changed", {}).get("value")
    new_value = change.get("string_map_data", {}).get("New Value", {}).get("value")
    change_date = change.get("string_map_data", {}).get("Change Date", {}).get("value")

    # Format the change date to YYYY-MM-DD
    if change_date:
        change_date = change_date[:10]

    # Append the profile change to the list
    profile_changes_list.append([changed, new_value, change_date])

# Write the profile changes to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Changed", "New Value", "Change Date"])
    writer.writerows(profile_changes_list)

print("Profile changes written to query_responses/results.csv")
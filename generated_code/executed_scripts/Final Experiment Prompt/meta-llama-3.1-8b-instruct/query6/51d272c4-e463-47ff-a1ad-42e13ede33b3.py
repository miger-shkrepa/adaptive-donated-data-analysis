import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Define the file path
file_path = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")

# Check if the file exists
if not os.path.exists(file_path):
    # If the file does not exist, return a CSV file with only the column headers
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Changed", "New Value", "Change Date"])
    print("Error: The file 'profile_changes.json' does not exist.")
    exit()

# Open the file and load the JSON data
with open(file_path, "r") as f:
    data = json.load(f)

# Initialize an empty list to store the changes
changes = []

# Iterate over the changes
for change in data["profile_profile_change"]:
    # Extract the changed, new value, and change date
    changed = change.get("Vorheriger Wert", "")  # Use 'Vorheriger Wert' instead of 'Changed'
    new_value = change.get("New Value", "")
    change_date = change.get("Change Date", "")

    # Format the change date to YYYY-MM-DD
    if change_date:
        change_date = change_date[:10]

    # Append the change to the list
    changes.append([changed, new_value, change_date])

# Write the changes to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Changed", "New Value", "Change Date"])
    writer.writerows(changes)

print("Query completed successfully.")
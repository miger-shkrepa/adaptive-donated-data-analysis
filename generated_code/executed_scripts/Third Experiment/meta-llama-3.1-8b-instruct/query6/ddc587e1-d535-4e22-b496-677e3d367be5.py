import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list to store the changes
changes = []

# Iterate over the personal information
for file in os.listdir(root_dir):
    if file.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, file), 'r') as f:
            # Load the JSON data
            data = json.load(f)

            # Check if the file contains the required information
            if "profile_profile_change" in data["structure"]["profile_changes"]:
                # Iterate over the changes
                for change in data["structure"]["profile_profile_change"]:
                    # Extract the required information
                    changed = change["string_map_data"]["Changed"]["value"]
                    new_value = change["string_map_data"]["New Value"]["value"]
                    change_date = change["string_map_data"]["Change Date"]["value"]

                    # Add the change to the list
                    changes.append([changed, new_value, change_date])

# Create the CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(["Changed", "New Value", "Change Date"])

    # Write the changes
    writer.writerows(changes)
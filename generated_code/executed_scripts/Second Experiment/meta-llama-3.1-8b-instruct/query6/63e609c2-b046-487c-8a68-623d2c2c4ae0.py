import csv
import os
import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list of changes
changes = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON file contains Instagram profile information
            if "instagram_profile_information.json" in filename:
                # Iterate over the profile account insights
                for insight in data["profile_account_insights"]:
                    # Check if the insight contains contact syncing information
                    if "Contact Syncing" in insight["string_map_data"]:
                        # Extract the contact syncing information
                        contact_syncing = insight["string_map_data"]["Contact Syncing"]["value"]

                        # Extract the change date
                        change_date = datetime.datetime.fromtimestamp(int(insight["string_map_data"]["Contact Syncing"]["timestamp"])).strftime("%Y-%m-%d")

                        # Add the change to the list of changes
                        changes.append((filename, contact_syncing, change_date))

# Write the changes to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Changed", "New Value", "Change Date"])
    writer.writerows(changes)
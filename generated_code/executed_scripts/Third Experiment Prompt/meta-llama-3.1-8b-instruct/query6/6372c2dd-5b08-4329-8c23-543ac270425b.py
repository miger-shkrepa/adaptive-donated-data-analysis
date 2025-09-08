import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list of changes
changes = []

# Iterate over the 'personal_information' directory
for filename in os.listdir(os.path.join(root_dir, "personal_information")):
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, "personal_information", filename), "r") as f:
            data = json.load(f)

            # Check if the file contains the required structure
            if "profile_user" in data["structure"]:
                # Iterate over the 'profile_user' structure
                for item in data["structure"]["profile_user"]:
                    # Check if the item contains the required fields
                    if "string_map_data" in item and "Benutzername" in item["string_map_data"] and "Geburtsdatum" in item["string_map_data"] and "Geschlecht" in item["string_map_data"] and "Methode zur Bestätigung der Telefonnummer" in item["string_map_data"] and "Name" in item["string_map_data"] and "Privates Konto" in item["string_map_data"] and "Telefonnummer" in item["string_map_data"] and "Telefonnummer bestätigt" in item["string_map_data"]:
                        # Extract the changes
                        changed = item["string_map_data"]["Benutzername"]["value"]
                        new_value = item["string_map_data"]["Geburtsdatum"]["value"]
                        change_date = item["string_map_data"]["Geschlecht"]["value"]

                        # Add the change to the list
                        changes.append([changed, new_value, change_date])

# Write the changes to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Changed", "New Value", "Change Date"])
    writer.writerows(changes)
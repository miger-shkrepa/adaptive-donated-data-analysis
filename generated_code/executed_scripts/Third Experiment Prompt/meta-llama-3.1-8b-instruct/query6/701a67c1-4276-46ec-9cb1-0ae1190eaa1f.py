import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list to store the results
results = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), "r") as f:
            # Load the JSON data
            data = json.load(f)

            # Check if the JSON data has the required structure
            if "personal_information" in data and "account_information.json" in data["personal_information"]:
                # Open the account information JSON file
                with open(os.path.join(root_dir, "personal_information", "account_information.json"), "r") as f:
                    # Load the account information JSON data
                    account_info = json.load(f)

                    # Iterate over the account information data
                    for item in account_info["profile_account_insights"]:
                        # Extract the changed, new value, and change date
                        changed = item["string_map_data"]["Erstes LÃ¤nderkennzeichen"]["value"]
                        new_value = item["string_map_data"]["Name"]["value"]
                        change_date = item["string_map_data"]["Zeitpunkt der ersten Story"]["value"]

                        # Add the result to the list
                        results.append([changed, new_value, change_date])

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Changed", "New Value", "Change Date"])
    writer.writerows(results)
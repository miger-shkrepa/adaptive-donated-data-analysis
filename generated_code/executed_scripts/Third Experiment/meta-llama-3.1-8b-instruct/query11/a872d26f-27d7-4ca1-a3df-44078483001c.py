import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the account names
accounts = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON data contains the required information
            if "ads_information" in data and "ads_viewed.json" in data["ads_information"]["ads_and_topics"]:
                # Extract the account names from the JSON data
                for item in data["ads_information"]["ads_and_topics"]["ads_viewed.json"]["structure"]["impressions_history_ads_seen"]:
                    for key, value in item["string_map_data"].items():
                        if key == "Author":
                            accounts.append(value["value"])

# Write the account names to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account"])  # Write the column headers
    writer.writerows([(account,) for account in accounts])  # Write the account names
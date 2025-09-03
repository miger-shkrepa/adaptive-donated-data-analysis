import os
import csv
import json

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store company names
company_names = []

# Define the paths to the relevant JSON files
json_files = [
    os.path.join(root_dir, "logged_information", "policy_updates_and_permissions", "no-data.txt"),
    os.path.join(root_dir, "media", "monetization", "eligibility.json")
]

# Iterate over the JSON files
for json_file in json_files:
    # Check if the JSON file exists
    if os.path.exists(json_file):
        # Load the JSON data
        with open(json_file, 'r') as f:
            data = json.load(f)

        # Extract the company names based on the structure of each JSON file
        if "monetization_eligibility" in data:
            for item in data["monetization_eligibility"]:
                if "string_map_data" in item and "Name des Produkts" in item["string_map_data"]:
                    company_names.append(item["string_map_data"]["Name des Produkts"]["value"])
        # Add more conditions here if necessary to extract company names from other JSON files

# Write the company names to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name"])
    for name in company_names:
        writer.writerow([name])
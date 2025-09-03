import os
import csv
import json

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store company names
company_names = []

# Define the list of JSON files that may contain company information
json_files = ["relationships_follow_requests_received.json", "hide_story_from.json", "removed_suggestions.json", "restricted_accounts.json"]

# Iterate over the JSON files
for json_file in json_files:
    file_path = os.path.join(root_dir, json_file)

    # Check if the file exists
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Extract company names from the JSON data
        for item in data["structure"]["relationships_follow_requests_received"]:
            for string_data in item["string_list_data"]:
                company_names.append(string_data["value"])
    else:
        print(f"Warning: {json_file} not found in the directory.")

# Save the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name"])
    for name in company_names:
        writer.writerow([name])
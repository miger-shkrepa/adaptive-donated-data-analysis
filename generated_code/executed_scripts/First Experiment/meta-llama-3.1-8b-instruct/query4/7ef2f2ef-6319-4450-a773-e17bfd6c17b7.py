import os
import csv
import json

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the company names
company_names = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Construct the full path to the file
    filepath = os.path.join(root_dir, filename)

    # Check if the file is a JSON file
    if filename.endswith(".json"):
        try:
            # Open the JSON file and load its contents
            with open(filepath, 'r') as file:
                data = json.load(file)

            # Check if the JSON file contains information about Instagram activity or information
            if "your_instagram_activity" in data:
                # Extract the company name from the JSON data
                company_name = "Instagram"

                # Add the company name to the list
                company_names.append(company_name)

        except json.JSONDecodeError:
            # Raise a ValueError if the JSON file is malformed
            raise ValueError("ValueError: The JSON file is malformed.")

# Write the company names to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name"])  # Header row
    writer.writerows([[company_name] for company_name in company_names])
import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the company names
company_names = []

# Iterate over the directory structure
for dirpath, dirnames, filenames in os.walk(root_dir):
    # Check if the current directory is 'your_instagram_activity'
    if dirpath.endswith('your_instagram_activity'):
        # Iterate over the files in the current directory
        for filename in filenames:
            # Check if the file is a JSON file
            if filename.endswith('.json'):
                # Open the JSON file
                with open(os.path.join(dirpath, filename), 'r') as f:
                    # Load the JSON data
                    data = json.load(f)
                    # Check if the JSON data has a 'structure' key
                    if 'structure' in data:
                        # Iterate over the structure
                        for item in data['structure']:
                            # Check if the item has a 'media_map_data' key
                            if 'media_map_data' in item:
                                # Get the company name from the 'media_map_data' key
                                company_name = item['media_map_data'].get('Company', '')
                                # Add the company name to the list
                                company_names.append(company_name)

# Write the company names to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Company Name'])
    writer.writerows([[company_name] for company_name in company_names])
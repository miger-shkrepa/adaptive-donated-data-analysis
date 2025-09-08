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
    # Check if the current directory is 'instagram_ads_and_businesses'
    if dirpath.endswith('instagram_ads_and_businesses'):
        # Iterate over the files in the current directory
        for filename in filenames:
            # Check if the file is 'advertisers_using_your_activity_or_information.json'
            if filename == 'advertisers_using_your_activity_or_information.json':
                # Open the file and load the JSON data
                with open(os.path.join(dirpath, filename), 'r') as f:
                    data = json.load(f)
                # Iterate over the 'ig_custom_audiences_all_types' list
                for item in data['ig_custom_audiences_all_types']:
                    # Extract the company name from the 'advertiser_name' key
                    company_name = item['advertiser_name']
                    # Add the company name to the list
                    company_names.append(company_name)

# Write the company names to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Company Name'])
    writer.writerows([[company_name] for company_name in company_names])
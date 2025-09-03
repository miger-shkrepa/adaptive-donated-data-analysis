import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the company names
companies = []

# Define the path to the JSON file
json_file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")

# Check if the JSON file exists
if os.path.exists(json_file_path):
    # Open the JSON file
    with open(json_file_path, 'r') as f:
        # Load the JSON data
        data = json.load(f)

        # Check if the 'ig_custom_audiences_all_types' key exists in the data
        if 'ig_custom_audiences_all_types' in data:
            # Iterate over the list of advertisers
            for advertiser in data['ig_custom_audiences_all_types']:
                # Check if the 'advertiser_name' key exists in the advertiser data
                if 'advertiser_name' in advertiser:
                    # Add the advertiser name to the list of companies
                    companies.append(advertiser['advertiser_name'])

# Define the path to the output CSV file
output_file_path = "query_responses/results.csv"

# Open the output CSV file
with open(output_file_path, 'w', newline='') as f:
    # Create a CSV writer
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["Company Name"])

    # Write the company names to the CSV file
    for company in companies:
        writer.writerow([company])
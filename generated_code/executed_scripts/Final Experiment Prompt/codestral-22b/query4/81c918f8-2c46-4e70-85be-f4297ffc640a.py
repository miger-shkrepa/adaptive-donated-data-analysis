import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Initialize an empty list to store the company names
company_names = []

# Construct the path to the JSON file
json_file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")

# Check if the file exists
if not os.path.exists(json_file_path):
    raise FileNotFoundError("FileNotFoundError: The JSON file does not exist.")

# Open the JSON file
with open(json_file_path, 'r', encoding='utf-8') as file:
    # Load the JSON data
    data = json.load(file)

    # Check if the 'ig_custom_audiences_all_types' key exists
    if 'ig_custom_audiences_all_types' in data:
        # Iterate over the list of dictionaries
        for item in data['ig_custom_audiences_all_types']:
            # Check if the 'advertiser_name' key exists
            if 'advertiser_name' in item:
                # Add the company name to the list
                company_names.append(item['advertiser_name'])

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(["Company Name"])
    # Write the company names
    for name in company_names:
        writer.writerow([name])
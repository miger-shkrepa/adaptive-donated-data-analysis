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
for key, value in json.loads(open(os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json"), encoding='utf-8').read()).items():
    # Check if the key is 'ig_custom_audiences_all_types'
    if key == 'ig_custom_audiences_all_types':
        # Iterate over the list of advertisers
        for advertiser in value:
            # Extract the company name from the advertiser's name
            company_name = advertiser['advertiser_name']
            # Add the company name to the list
            company_names.append(company_name)

# Write the company names to a CSV file
with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name"])  # Write the header
    for company_name in company_names:
        writer.writerow([company_name])  # Write each company name
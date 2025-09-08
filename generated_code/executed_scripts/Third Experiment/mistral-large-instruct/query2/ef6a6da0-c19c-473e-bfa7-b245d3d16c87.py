import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("Error: The root directory does not exist.")

# Initialize the CSV writer
with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Company Name", "Number of Ads Viewed"])

    # Check if the necessary files exist
    ads_file_path = os.path.join(root_dir, 'your_instagram_activity', 'ads', 'ads_viewed.json')
    if not os.path.exists(ads_file_path):
        # If the ads file does not exist, write only the headers and exit
        writer.writerow([])
        exit()

    # Read the ads viewed data
    try:
        with open(ads_file_path, 'r') as ads_file:
            ads_data = json.load(ads_file)
    except json.JSONDecodeError:
        raise ValueError("Error: The ads_viewed.json file is not a valid JSON.")

    # Process the ads data
    ads_count = {}
    for ad in ads_data.get('ads_viewed', []):
        company_name = ad.get('title', 'Unknown Company')
        if company_name in ads_count:
            ads_count[company_name] += 1
        else:
            ads_count[company_name] = 1

    # Write the results to the CSV file
    for company, count in ads_count.items():
        writer.writerow([company, count])
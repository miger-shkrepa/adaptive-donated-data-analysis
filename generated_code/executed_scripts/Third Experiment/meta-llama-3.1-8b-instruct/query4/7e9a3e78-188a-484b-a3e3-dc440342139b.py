import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list of companies
companies = []

# Iterate over the directory structure
for item in os.listdir(root_dir):
    item_path = os.path.join(root_dir, item)
    if os.path.isdir(item_path):
        # Check if the item is the 'instagram_ads_and_businesses' directory
        if item == 'instagram_ads_and_businesses':
            # Iterate over the files in the 'instagram_ads_and_businesses' directory
            for file in os.listdir(item_path):
                file_path = os.path.join(item_path, file)
                if file.endswith('.json'):
                    # Open the JSON file and parse its contents
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        # Check if the file contains the required data
                        if 'ig_custom_audiences_all_types' in data['structure']:
                            # Extract the company names from the data
                            for company in data['structure']['ig_custom_audiences_all_types']:
                                companies.append(company['advertiser_name'])

# Write the companies to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Company Name'])  # Write the header
    for company in companies:
        writer.writerow([company])
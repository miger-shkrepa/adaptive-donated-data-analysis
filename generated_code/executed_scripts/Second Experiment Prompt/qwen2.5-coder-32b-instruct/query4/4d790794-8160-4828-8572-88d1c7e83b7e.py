import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Define the path to the JSON file
json_file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")

# Initialize a list to store company names
company_names = []

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Check if the JSON file exists
if os.path.exists(json_file_path):
    try:
        # Read the JSON file
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            
            # Extract the company names
            if 'ig_custom_audiences_all_types' in data:
                for advertiser in data['ig_custom_audiences_all_types']:
                    if 'advertiser_name' in advertiser:
                        company_names.append(advertiser['advertiser_name'])
            else:
                raise ValueError("ValueError: The required data structure is missing in the JSON file.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The JSON file is not properly formatted.")
else:
    # If the file does not exist, treat its contribution as 0 and continue processing
    print("Warning: The required JSON file does not exist. Continuing with an empty list of company names.")

# Write the company names to the CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Company Name'])
    for company in company_names:
        writer.writerow([company])
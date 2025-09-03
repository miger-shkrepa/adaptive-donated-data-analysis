import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the company names
company_names = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as f:
            # Load the JSON data
            data = json.load(f)
            
            # Check if the JSON data contains the required information
            if "ads_information" in data and "instagram_ads_and_businesses" in data["ads_information"]:
                # Extract the company names from the JSON data
                company_names.extend([item["advertiser_name"] for item in data["ads_information"]["instagram_ads_and_businesses"]["advertisers_using_your_activity_or_information.json"]["structure"]["ig_custom_audiences_all_types"]])

# Write the company names to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name"])
    writer.writerows([[company] for company in company_names])
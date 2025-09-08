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
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON data contains the required information
            if "instagram_ads_and_businesses" in data and "advertisers_using_your_activity_or_information.json" in data["instagram_ads_and_businesses"]:
                # Extract the company names from the JSON data
                for advertiser in data["instagram_ads_and_businesses"]["advertisers_using_your_activity_or_information.json"]["ig_custom_audiences_all_types"]:
                    company_names.append(advertiser["advertiser_name"])

# Write the company names to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name"])  # Write the column headers
    writer.writerows([[company] for company in company_names])  # Write the company names

print("Query completed successfully.")
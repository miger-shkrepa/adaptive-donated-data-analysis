import csv
import os

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the company names
company_names = []

# Iterate through the directory structure
for item in os.listdir(root_dir):
    # Check if the item is a file
    if os.path.isfile(os.path.join(root_dir, item)):
        # Check if the file is a JSON file
        if item.endswith(".json"):
            # Open the JSON file
            with open(os.path.join(root_dir, item), 'r') as f:
                # Load the JSON data
                data = json.load(f)
                # Check if the JSON data contains the required information
                if "instagram_ads_and_businesses" in data and "advertisers_using_your_activity_or_information.json" in data["instagram_ads_and_businesses"]:
                    # Extract the company names
                    for advertiser in data["instagram_ads_and_businesses"]["advertisers_using_your_activity_or_information.json"]["ig_custom_audiences_all_types"]:
                        company_names.append(advertiser["advertiser_name"])
                elif "instagram_ads_and_businesses" in data and "other_categories_used_to_reach_you.json" in data["instagram_ads_and_businesses"]:
                    # Extract the company names
                    company_names.append("Other categories used to reach you")
                elif "instagram_ads_and_businesses" in data and "subscription_for_no_ads.json" in data["instagram_ads_and_businesses"]:
                    # Extract the company names
                    company_names.append("Subscription for no ads")

# Write the company names to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name"])  # Write the column headers
    for company in company_names:
        writer.writerow([company])
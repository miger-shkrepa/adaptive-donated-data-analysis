import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty dictionary to store the ad counts
ad_counts = {}

# Define the path to the ads_viewed.json file
ads_file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")

# Check if the ads_viewed.json file exists
if os.path.exists(ads_file_path):
    # Open the ads_viewed.json file
    with open(ads_file_path, "r") as f:
        # Load the JSON data
        data = json.load(f)

        # Check if the JSON data has the expected structure
        if "impressions_history_ads_seen" in data:
            # Iterate over the ads seen
            for ad in data["impressions_history_ads_seen"]:
                # Check if the ad has the expected structure
                if "string_map_data" in ad and "Author" in ad["string_map_data"]:
                    # Extract the company name
                    company_name = ad["string_map_data"]["Author"]["value"]

                    # Increment the ad count for the company
                    if company_name in ad_counts:
                        ad_counts[company_name] += 1
                    else:
                        ad_counts[company_name] = 1

# Define the path to the results.csv file
results_file_path = "query_responses/results.csv"

# Create the query_responses directory if it doesn't exist
os.makedirs(os.path.dirname(results_file_path), exist_ok=True)

# Write the results to the results.csv file
with open(results_file_path, "w", newline="") as f:
    # Create a CSV writer
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["Company Name", "Number of Ads Viewed"])

    # Write the ad counts for each company
    for company_name, ad_count in ad_counts.items():
        writer.writerow([company_name, ad_count])
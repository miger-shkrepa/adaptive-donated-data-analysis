import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list of companies and their ad views
companies = []

# Iterate over the ads information directory
for company in os.listdir(os.path.join(root_dir, "ads_information", "ads_and_topics")):
    # Check if the company directory exists
    company_dir = os.path.join(root_dir, "ads_information", "ads_and_topics", company)
    if os.path.isdir(company_dir):
        # Initialize the ad views for the company
        ad_views = 0

        # Iterate over the JSON files in the company directory
        for file in os.listdir(company_dir):
            if file.endswith(".json"):
                # Open the JSON file
                with open(os.path.join(company_dir, file), "r") as f:
                    # Load the JSON data
                    data = json.load(f)

                    # Check if the JSON file contains ad view data
                    if "impressions_history_ads_seen" in data["structure"]:
                        # Increment the ad views for the company
                        ad_views += len(data["structure"]["impressions_history_ads_seen"])

        # Add the company and its ad views to the list
        companies.append((company, ad_views))

# Write the companies and their ad views to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    writer.writerows(companies)
import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the company names
companies = []

# Define the path to the relevant directory
ads_info_dir = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses")

# Check if the directory exists
if os.path.exists(ads_info_dir):
    # Define the path to the relevant file
    file_path = os.path.join(ads_info_dir, "advertisers_using_your_activity_or_information.json")

    # Check if the file exists
    if os.path.exists(file_path):
        # Open the file and load the JSON data
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Extract the company names
        for item in data["ig_custom_audiences_all_types"]:
            companies.append(item["advertiser_name"])

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Company Name"])
    for company in companies:
        writer.writerow([company])
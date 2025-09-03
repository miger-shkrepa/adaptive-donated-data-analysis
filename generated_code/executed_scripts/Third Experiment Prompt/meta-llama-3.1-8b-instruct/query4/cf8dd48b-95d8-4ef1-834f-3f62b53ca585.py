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
try:
    with open(os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json"), 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data["ig_custom_audiences_all_types"]:
            company_names.append(item["advertiser_name"])
except FileNotFoundError:
    raise FileNotFoundError("FileNotFoundError: The file 'advertisers_using_your_activity_or_information.json' does not exist.")
except json.JSONDecodeError as e:
    raise ValueError("ValueError: The file 'advertisers_using_your_activity_or_information.json' is not a valid JSON.")

# Write the company names to a CSV file
with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name"])
    writer.writerows([[company] for company in company_names])
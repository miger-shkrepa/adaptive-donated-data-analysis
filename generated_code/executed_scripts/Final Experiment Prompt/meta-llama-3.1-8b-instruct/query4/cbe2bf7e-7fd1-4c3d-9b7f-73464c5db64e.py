import csv
import os
import json

# Set the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Set the file path
file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")

# Check if the file exists
if not os.path.exists(file_path):
    print("Error: The file 'advertisers_using_your_activity_or_information.json' does not exist.")
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name"])
    exit()

# Open the file and read the JSON data
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except ValueError as e:
    raise ValueError("ValueError: Failed to parse JSON file: " + str(e))

# Extract the company names from the JSON data
company_names = [entry['advertiser_name'] for entry in data['ig_custom_audiences_all_types'] if 'advertiser_name' in entry]

# Write the company names to a CSV file
with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name"])
    writer.writerows([[name] for name in company_names])
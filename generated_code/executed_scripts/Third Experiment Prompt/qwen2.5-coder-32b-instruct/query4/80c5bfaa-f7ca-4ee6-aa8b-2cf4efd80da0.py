import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Define the path to the JSON file
json_file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")

# Initialize a list to store company names
company_names = []

# Check if the JSON file exists
if not os.path.exists(json_file_path):
    # If the file does not exist, create an empty CSV with only the column header
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Company Name'])
    raise FileNotFoundError("FileNotFoundError: The required JSON file does not exist.")

# Read the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
except json.JSONDecodeError:
    raise ValueError("ValueError: The JSON file is not properly formatted.")

# Extract company names from the JSON data
try:
    for entry in data.get("ig_custom_audiences_all_types", []):
        company_names.append(entry.get("advertiser_name", ""))
except Exception as e:
    raise ValueError(f"ValueError: Error parsing the JSON data - {str(e)}")

# Write the company names to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Company Name'])
    for name in company_names:
        writer.writerow([name])
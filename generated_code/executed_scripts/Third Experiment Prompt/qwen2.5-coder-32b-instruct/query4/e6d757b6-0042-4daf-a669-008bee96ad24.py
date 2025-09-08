import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Define the path to the JSON file
json_file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")

# Initialize a list to store company names
company_names = []

try:
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    # Check if the JSON file exists
    if not os.path.exists(json_file_path):
        raise FileNotFoundError("FileNotFoundError: The JSON file does not exist.")
    
    # Open and read the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Extract company names from the JSON data
    if "ig_custom_audiences_all_types" in data:
        for advertiser in data["ig_custom_audiences_all_types"]:
            if "advertiser_name" in advertiser:
                company_names.append(advertiser["advertiser_name"])
    else:
        raise ValueError("ValueError: The expected structure in the JSON file is missing.")
    
except FileNotFoundError as e:
    print(e)
except ValueError as e:
    print(e)
except Exception as e:
    print(f"Error: An unexpected error occurred: {e}")

# Define the path for the output CSV file
output_csv_path = 'query_responses/results.csv'

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

# Write the company names to the CSV file
with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name"])
    for name in company_names:
        writer.writerow([name])
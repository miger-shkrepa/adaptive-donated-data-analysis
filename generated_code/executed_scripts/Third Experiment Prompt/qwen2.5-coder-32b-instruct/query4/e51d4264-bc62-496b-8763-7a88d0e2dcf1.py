import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Define the path to the JSON file containing advertisers information
advertisers_file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")

# Initialize a list to store company names
company_names = []

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Check if the advertisers file exists
if not os.path.exists(advertisers_file_path):
    # If the file does not exist, create an empty CSV with only the column headers
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name"])
    print("Advertisers file not found. Created an empty CSV with column headers.")
else:
    # Read the JSON file
    try:
        with open(advertisers_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Extract company names from the JSON data
        if "ig_custom_audiences_all_types" in data:
            for entry in data["ig_custom_audiences_all_types"]:
                if "advertiser_name" in entry:
                    company_names.append(entry["advertiser_name"])
    
    except json.JSONDecodeError:
        raise ValueError("ValueError: The advertisers file is not a valid JSON file.")
    
    # Write the company names to a CSV file
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name"])
        for name in company_names:

            writer.writerow([name])

print("CSV file with company names has been created.")
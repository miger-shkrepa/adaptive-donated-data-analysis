import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Define the path for the output CSV file
output_csv_path = 'query_responses/results.csv'

# Initialize a set to store unique company names
company_names = set()

# Function to recursively search for JSON files in the directory
def search_json_files(directory):
    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        if os.path.isdir(full_path):
            search_json_files(full_path)
        elif os.path.isfile(full_path) and full_path.endswith('.json'):
            try:
                with open(full_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    # Check for any keys that might contain company names
                    if 'apps_and_websites' in data:
                        for app in data['apps_and_websites']:
                            if 'company_name' in app:
                                company_names.add(app['company_name'])
            except (FileNotFoundError, ValueError) as e:
                print(f"Error: Failed to read file {full_path}. Reason: {e}")

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Check if the apps_and_websites_off_of_instagram directory exists
apps_and_websites_dir = os.path.join(root_dir, 'apps_and_websites_off_of_instagram')
if not os.path.exists(apps_and_websites_dir):
    print("Warning: The apps_and_websites_off_of_instagram directory does not exist. Continuing with an empty result.")

# Search for JSON files in the apps_and_websites_off_of_instagram directory
if os.path.exists(apps_and_websites_dir):
    search_json_files(apps_and_websites_dir)

# Ensure the output directory exists
output_dir = os.path.dirname(output_csv_path)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Write the results to a CSV file
with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Company Name'])
    for company in company_names:
        csvwriter.writerow([company])

print(f"Results saved to {output_csv_path}")
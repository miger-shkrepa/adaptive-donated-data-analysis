import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Initialize a dictionary to store the count of ads viewed per company
ads_count = {}

# Function to process JSON files and count ads
def process_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for entry in data.get('impressions_history_ads_seen', []):
                author = entry.get('string_map_data', {}).get('Author', {}).get('value', 'Unknown')
                if author in ads_count:
                    ads_count[author] += 1
                else:
                    ads_count[author] = 1
    except json.JSONDecodeError:
        raise ValueError("Error: Invalid JSON format in file {}".format(file_path))
    except FileNotFoundError:
        raise FileNotFoundError("Error: File {} does not exist.".format(file_path))

# Walk through the directory structure
try:
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file == 'ads_viewed.json':
                file_path = os.path.join(subdir, file)
                process_json_file(file_path)
except FileNotFoundError:
    raise FileNotFoundError("Error: The root directory does not exist.")

# Write the results to a CSV file
try:
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Company Name', 'Number of Ads Viewed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for company, count in ads_count.items():
            writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})
except Exception as e:
    raise ValueError("Error: Failed to write to CSV file. {}".format(str(e)))
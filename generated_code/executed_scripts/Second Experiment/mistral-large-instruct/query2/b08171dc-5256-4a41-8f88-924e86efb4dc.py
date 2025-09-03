import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to read JSON files
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: ValueError: The file {file_path} is not a valid JSON file.")

# Function to process ads_viewed.json
def process_ads_viewed(file_path):
    data = read_json_file(file_path)
    ads_seen = data.get('impressions_history_ads_seen', [])
    return ads_seen

# Function to process advertisers_using_your_activity_or_information.json
def process_advertisers(file_path):
    data = read_json_file(file_path)
    advertisers = data.get('ig_custom_audiences_all_types', [])
    return advertisers

# Main function to generate the CSV
def generate_csv():
    ads_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')
    advertisers_path = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'advertisers_using_your_activity_or_information.json')

    try:
        ads_seen = process_ads_viewed(ads_viewed_path)
    except Exception as e:
        print(e)
        ads_seen = []

    try:
        advertisers = process_advertisers(advertisers_path)
    except Exception as e:
        print(e)
        advertisers = []

    # Create a dictionary to count ads viewed by company
    ads_count = {}
    for ad in ads_seen:
        author = ad.get('string_map_data', {}).get('Author', {}).get('value', 'Unknown')
        if author in ads_count:
            ads_count[author] += 1
        else:
            ads_count[author] = 1

    # Write the results to a CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Company Name', 'Number of Ads Viewed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for company, count in ads_count.items():
            writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})

# Execute the main function
generate_csv()
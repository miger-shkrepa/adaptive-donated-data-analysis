import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Function to read JSON file
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to get the number of ads viewed
def get_ads_viewed_count(ads_viewed_data):
    if 'impressions_history_ads_seen' in ads_viewed_data:
        return len(ads_viewed_data['impressions_history_ads_seen'])
    return 0

# Function to get the list of advertisers
def get_advertisers(advertisers_data):
    if 'ig_custom_audiences_all_types' in advertisers_data:
        return [advertiser['advertiser_name'] for advertiser in advertisers_data['ig_custom_audiences_all_types']]
    return []

# Main function to process the data and generate the CSV
def process_data(root_dir):
    ads_viewed_file_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')
    advertisers_file_path = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'advertisers_using_your_activity_or_information.json')
    
    ads_viewed_count = 0
    advertisers = set()
    
    # Check and process ads_viewed.json
    if os.path.exists(ads_viewed_file_path):
        ads_viewed_data = read_json_file(ads_viewed_file_path)
        ads_viewed_count = get_ads_viewed_count(ads_viewed_data)
    else:
        print(f"Warning: The file {ads_viewed_file_path} does not exist. Continuing with 0 ads viewed.")
    
    # Check and process advertisers_using_your_activity_or_information.json
    if os.path.exists(advertisers_file_path):
        advertisers_data = read_json_file(advertisers_file_path)
        advertisers.update(get_advertisers(advertisers_data))
    else:
        print(f"Warning: The file {advertisers_file_path} does not exist. Continuing with no advertisers.")
    
    # Prepare the CSV data
    csv_data = []
    for advertiser in advertisers:
        csv_data.append([advertiser, ads_viewed_count])
    
    # Write the CSV file
    try:
        os.makedirs(os.path.dirname('query_responses/results.csv'), exist_ok=True)
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Company Name', 'Number of Ads Viewed'])
            csvwriter.writerows(csv_data)
    except Exception as e:
        raise Exception(f"Error: Failed to write the CSV file. {str(e)}")

# Execute the main function
try:
    process_data(root_dir)
except Exception as e:
    print(e)
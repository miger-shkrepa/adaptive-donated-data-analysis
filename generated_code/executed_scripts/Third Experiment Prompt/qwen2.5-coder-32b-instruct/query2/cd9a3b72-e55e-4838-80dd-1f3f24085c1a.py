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

# Function to get the path of a file
def get_file_path(root_dir, *subdirs):
    return os.path.join(root_dir, *subdirs)

# Initialize the result dictionary
company_ads_count = {}

# Path to the ads_viewed.json file
ads_viewed_path = get_file_path(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")

# Path to the advertisers_using_your_activity_or_information.json file
advertisers_path = get_file_path(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")

# Read the ads_viewed.json file if it exists
if os.path.exists(ads_viewed_path):
    ads_viewed_data = read_json_file(ads_viewed_path)
    for entry in ads_viewed_data.get("impressions_history_ads_seen", []):
        string_map_data = entry.get("string_map_data", {})
        author = string_map_data.get("Author", {}).get("value", "Unknown")
        if author not in company_ads_count:
            company_ads_count[author] = 0
        company_ads_count[author] += 1

# Read the advertisers_using_your_activity_or_information.json file if it exists
if os.path.exists(advertisers_path):
    advertisers_data = read_json_file(advertisers_path)
    for entry in advertisers_data.get("ig_custom_audiences_all_types", []):
        advertiser_name = entry.get("advertiser_name", "Unknown")
        if advertiser_name not in company_ads_count:
            company_ads_count[advertiser_name] = 0

# Prepare the CSV file path
csv_file_path = 'query_responses/results.csv'

# Ensure the directory exists
os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

# Write the results to the CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Company Name", "Number of Ads Viewed"])
    for company, count in company_ads_count.items():
        csvwriter.writerow([company, count])
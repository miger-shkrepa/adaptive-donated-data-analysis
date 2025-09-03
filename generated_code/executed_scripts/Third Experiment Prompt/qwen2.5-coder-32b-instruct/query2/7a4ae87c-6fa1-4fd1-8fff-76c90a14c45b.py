import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Define the path to the ads_viewed.json file
ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")

# Initialize a dictionary to store the count of ads viewed per company
ads_count = {}

# Check if the ads_viewed.json file exists
if not os.path.exists(ads_viewed_path):
    # If the file does not exist, create an empty CSV file with the headers
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Company Name', 'Number of Ads Viewed'])
    raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")

# Read the ads_viewed.json file
try:
    with open(ads_viewed_path, 'r', encoding='utf-8') as file:
        ads_data = json.load(file)
except json.JSONDecodeError:
    raise ValueError("ValueError: The ads_viewed.json file is not a valid JSON file.")

# Check if the required structure exists in the JSON data
if 'impressions_history_ads_seen' not in ads_data:
    raise ValueError("ValueError: The ads_viewed.json file does not contain the expected structure.")

# Process the ads viewed data
for ad in ads_data['impressions_history_ads_seen']:
    if 'string_map_data' in ad and 'Author' in ad['string_map_data']:
        author = ad['string_map_data']['Author']['value']
        if author in ads_count:
            ads_count[author] += 1
        else:
            ads_count[author] = 1

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Company Name', 'Number of Ads Viewed'])
    for company, count in ads_count.items():
        csvwriter.writerow([company, count])
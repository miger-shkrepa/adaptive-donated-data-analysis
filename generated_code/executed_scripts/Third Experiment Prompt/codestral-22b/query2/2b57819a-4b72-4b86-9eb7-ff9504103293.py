import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

ads_viewed = {}

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file == "ads_viewed.json":
            try:
                with open(os.path.join(root, file), 'r') as f:
                    data = json.load(f)
                    for ad in data.get('impressions_history_ads_seen', []):
                        company = ad.get('string_map_data', {}).get('Company', {}).get('value', 'Unknown')
                        if company in ads_viewed:
                            ads_viewed[company] += 1
                        else:
                            ads_viewed[company] = 1
            except FileNotFoundError:
                print(f"FileNotFoundError: The file {file} does not exist.")
            except json.JSONDecodeError:
                print(f"JSONDecodeError: The file {file} is not a valid JSON file.")

with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Company Name', 'Number of Ads Viewed'])
    for company, count in ads_viewed.items():
        writer.writerow([company, count])
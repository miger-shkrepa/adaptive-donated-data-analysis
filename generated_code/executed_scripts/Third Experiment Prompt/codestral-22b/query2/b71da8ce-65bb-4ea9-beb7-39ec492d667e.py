import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

ads_viewed_data = []

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file == "ads_viewed.json":
            try:
                with open(os.path.join(root, file), 'r') as f:
                    data = json.load(f)
                    for ad in data["impressions_history_ads_seen"]:
                        company_name = ad["string_map_data"]["Author"]["value"]
                        ads_viewed_data.append(company_name)
            except Exception as e:
                print(f"Error: {e}")

ads_viewed_count = {company: ads_viewed_data.count(company) for company in ads_viewed_data}

with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Company Name', 'Number of Ads Viewed']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for company, count in ads_viewed_count.items():
        writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})
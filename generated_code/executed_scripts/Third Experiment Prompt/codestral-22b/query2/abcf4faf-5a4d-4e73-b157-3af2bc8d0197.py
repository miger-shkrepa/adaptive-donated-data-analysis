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
                    for ad in data["impressions_history_ads_seen"]:
                        if "Author" in ad["string_map_data"]:
                            author = ad["string_map_data"]["Author"]["value"]
                            if author in ads_viewed:
                                ads_viewed[author] += 1
                            else:
                                ads_viewed[author] = 1
            except Exception as e:
                print(f"Error: {e}")

with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Company Name', 'Number of Ads Viewed']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for company, count in ads_viewed.items():
        writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})
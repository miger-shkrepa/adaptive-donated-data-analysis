import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

ads_data = {}

ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")

if os.path.exists(ads_viewed_path):
    with open(ads_viewed_path, 'r') as f:
        ads_viewed = json.load(f)

    for ad in ads_viewed["impressions_history_ads_seen"]:
        if "Author" in ad["string_map_data"]:
            author = ad["string_map_data"]["Author"]["value"]
            if author in ads_data:
                ads_data[author] += 1
            else:
                ads_data[author] = 1

with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Company Name', 'Number of Ads Viewed']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for company, count in ads_data.items():
        writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})
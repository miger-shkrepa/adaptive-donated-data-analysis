import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")

if not os.path.exists(ads_viewed_path):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name", "Number of Ads Viewed"])
    raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")

with open(ads_viewed_path, 'r') as f:
    ads_viewed = json.load(f)

ads_data = ads_viewed.get("impressions_history_ads_seen", [])

company_ads = {}
for ad in ads_data:
    author = ad.get("string_map_data", {}).get("Author", {}).get("value", "")
    if author:
        if author in company_ads:
            company_ads[author] += 1
        else:
            company_ads[author] = 1

with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    for company, count in company_ads.items():
        writer.writerow([company, count])
import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

ads_viewed_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")

if not os.path.exists(ads_viewed_file):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name", "Number of Ads Viewed"])
    exit()

with open(ads_viewed_file, 'r') as f:
    data = json.load(f)

ads_viewed = data.get("impressions_history_ads_seen", [])

company_ads_count = {}
for ad in ads_viewed:
    author = ad.get("string_map_data", {}).get("Author", {}).get("value", "")
    if author in company_ads_count:
        company_ads_count[author] += 1
    else:
        company_ads_count[author] = 1

with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    for company, count in company_ads_count.items():
        writer.writerow([company, count])
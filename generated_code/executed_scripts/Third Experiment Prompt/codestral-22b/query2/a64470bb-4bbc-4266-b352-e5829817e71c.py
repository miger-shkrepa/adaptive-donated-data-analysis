import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

ads_viewed_data = []

ads_and_topics_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")

if os.path.exists(ads_and_topics_dir):
    ads_viewed_file = os.path.join(ads_and_topics_dir, "ads_viewed.json")

    if os.path.exists(ads_viewed_file):
        with open(ads_viewed_file, 'r') as f:
            data = json.load(f)

        for ad in data["impressions_history_ads_seen"]:
            author = ad["string_map_data"]["Author"]["value"]
            ads_viewed_data.append(author)

company_ads_viewed = {}
for company in ads_viewed_data:
    if company in company_ads_viewed:
        company_ads_viewed[company] += 1
    else:
        company_ads_viewed[company] = 1

with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Company Name', 'Number of Ads Viewed']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for company, count in company_ads_viewed.items():
        writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})
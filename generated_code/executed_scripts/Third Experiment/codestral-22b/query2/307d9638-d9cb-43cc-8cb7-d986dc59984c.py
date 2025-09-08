import os
import json
import csv

root_dir = "root_dir"
ads_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

if not os.path.exists(ads_file):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name", "Number of Ads Viewed"])
else:
    with open(ads_file, 'r') as f:
        data = json.load(f)

    ads_viewed = data["impressions_history_ads_seen"]
    company_ads = {}

    for ad in ads_viewed:
        if "Author" in ad["string_map_data"]:
            company = ad["string_map_data"]["Author"]["value"]
            if company in company_ads:
                company_ads[company] += 1
            else:
                company_ads[company] = 1

    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name", "Number of Ads Viewed"])
        for company, count in company_ads.items():
            writer.writerow([company, count])
import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

ads_data = []

ads_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
if not os.path.exists(ads_dir):
    ads_data.append(["Company Name", "Number of Ads Viewed"])
else:
    ads_viewed_file = os.path.join(ads_dir, "ads_viewed.json")
    if os.path.exists(ads_viewed_file):
        with open(ads_viewed_file, "r") as f:
            data = json.load(f)
            ads_viewed = data["impressions_history_ads_seen"]
            company_count = {}
            for ad in ads_viewed:
                company = ad["string_map_data"]["Author"]["value"]
                if company in company_count:
                    company_count[company] += 1
                else:
                    company_count[company] = 1
            ads_data = [["Company Name", "Number of Ads Viewed"]] + [[company, count] for company, count in company_count.items()]
    else:
        ads_data.append(["Company Name", "Number of Ads Viewed"])

with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(ads_data)
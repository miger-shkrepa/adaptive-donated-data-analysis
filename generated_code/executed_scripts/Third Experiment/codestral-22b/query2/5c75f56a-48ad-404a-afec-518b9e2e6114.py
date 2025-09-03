import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

ads_viewed_dir = os.path.join(root_dir, "ads_information/ads_and_topics")

if not os.path.exists(ads_viewed_dir):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name", "Number of Ads Viewed"])
else:
    ads_viewed_count = {}
    for filename in os.listdir(ads_viewed_dir):
        if filename == "ads_viewed.json":
            file_path = os.path.join(ads_viewed_dir, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                for ad in data["impressions_history_ads_seen"]:
                    company = ad["string_map_data"]["Author"]["value"]
                    if company in ads_viewed_count:
                        ads_viewed_count[company] += 1
                    else:
                        ads_viewed_count[company] = 1

    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name", "Number of Ads Viewed"])
        for company, count in ads_viewed_count.items():
            writer.writerow([company, count])
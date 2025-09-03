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
else:
    with open(ads_viewed_file, 'r') as f:
        data = json.load(f)

    ads_viewed = data.get("impressions_history_ads_seen", [])
    ads_count = {}

    for ad in ads_viewed:
        string_map_data = ad.get("string_map_data", {})
        time_data = string_map_data.get("Time", {})
        value = time_data.get("value", "")
        company = value.split(" ")[0]  # assuming the company name is the first word in the value
        ads_count[company] = ads_count.get(company, 0) + 1

    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name", "Number of Ads Viewed"])
        for company, count in ads_count.items():
            writer.writerow([company, count])
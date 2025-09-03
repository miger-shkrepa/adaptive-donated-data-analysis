import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

ads_data = []

ads_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")

if os.path.exists(ads_dir):
    for filename in os.listdir(ads_dir):
        if filename == "ads_viewed.json":
            filepath = os.path.join(ads_dir, filename)
            with open(filepath, 'r') as f:
                data = json.load(f)
                for ad in data["impressions_history_ads_seen"]:
                    company = ad["string_map_data"]["Author"]["value"]
                    ads_data.append({"Company Name": company, "Number of Ads Viewed": 1})

output_file = "query_responses/results.csv"

with open(output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["Company Name", "Number of Ads Viewed"])
    writer.writeheader()
    for row in ads_data:
        writer.writerow(row)
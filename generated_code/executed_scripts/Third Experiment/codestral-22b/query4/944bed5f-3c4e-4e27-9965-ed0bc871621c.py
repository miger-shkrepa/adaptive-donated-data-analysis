import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

companies = set()

ads_folder = os.path.join(root_dir, "ads_information", "ads_and_topics")
for filename in os.listdir(ads_folder):
    if filename.endswith(".json"):
        filepath = os.path.join(ads_folder, filename)
        with open(filepath, 'r') as f:
            data = json.load(f)
            for item in data.get("impressions_history_ads_seen", []):
                author = item.get("string_map_data", {}).get("Author", {}).get("value")
                if author:
                    companies.add(author)

with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Company Name"])
    for company in companies:
        writer.writerow([company])
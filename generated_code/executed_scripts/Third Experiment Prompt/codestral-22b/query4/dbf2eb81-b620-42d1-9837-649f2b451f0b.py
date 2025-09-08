import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

companies = set()

ads_info_dir = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses")

if os.path.exists(ads_info_dir):
    ads_file = os.path.join(ads_info_dir, "advertisers_using_your_activity_or_information.json")
    if os.path.exists(ads_file):
        with open(ads_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data.get("ig_custom_audiences_all_types", []):
                companies.add(item.get("advertiser_name", ""))

with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name"])
    for company in companies:
        writer.writerow([company])
import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

companies = set()

ads_info_dir = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses")
if os.path.exists(ads_info_dir):
    for file_name in os.listdir(ads_info_dir):
        if file_name.endswith(".json"):
            file_path = os.path.join(ads_info_dir, file_name)
            with open(file_path, 'r') as f:
                data = json.load(f)
                if "ig_custom_audiences_all_types" in data:
                    for item in data["ig_custom_audiences_all_types"]:
                        if "advertiser_name" in item:
                            companies.add(item["advertiser_name"])

with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name"])
    for company in companies:
        writer.writerow([company])
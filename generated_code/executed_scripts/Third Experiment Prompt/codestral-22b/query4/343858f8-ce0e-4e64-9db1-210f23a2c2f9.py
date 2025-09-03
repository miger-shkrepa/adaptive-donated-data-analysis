import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

companies = set()

ads_information_dir = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses")
file_path = os.path.join(ads_information_dir, "advertisers_using_your_activity_or_information.json")

if os.path.exists(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
        for item in data.get("ig_custom_audiences_all_types", []):
            companies.add(item.get("advertiser_name", ""))

output_file = "query_responses/results.csv"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Company Name"])
    for company in companies:
        writer.writerow([company])
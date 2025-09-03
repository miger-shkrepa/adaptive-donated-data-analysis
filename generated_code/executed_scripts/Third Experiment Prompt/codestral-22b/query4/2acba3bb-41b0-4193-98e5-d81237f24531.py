import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

companies = set()

ads_information_dir = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses")
for filename in os.listdir(ads_information_dir):
    if filename.endswith(".json"):
        filepath = os.path.join(ads_information_dir, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "ig_custom_audiences_all_types" in data:
                    for item in data["ig_custom_audiences_all_types"]:
                        companies.add(item["advertiser_name"])
        except Exception as e:
            print(f"Error processing file {filepath}: {e}")

output_file = "query_responses/results.csv"
os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Company Name"])
    for company in companies:
        writer.writerow([company])
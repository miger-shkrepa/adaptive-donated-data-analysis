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
            with open(filepath, "r") as file:
                data = json.load(file)
                if "structure" in data and "ig_custom_audiences_all_types" in data["structure"]:
                    for item in data["structure"]["ig_custom_audiences_all_types"]:
                        if "advertiser_name" in item:
                            companies.add(item["advertiser_name"])
        except Exception as e:
            print(f"Error processing file {filepath}: {e}")

output_file = "query_responses/results.csv"

with open(output_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Company Name"])
    for company in companies:
        writer.writerow([company])
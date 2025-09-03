import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

ads_data = {}

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file == "ads_viewed.json":
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    for ad in data["impressions_history_ads_seen"]:
                        author = ad["string_map_data"].get("Author", {}).get("value", "Unknown")
                        if author in ads_data:
                            ads_data[author] += 1
                        else:
                            ads_data[author] = 1
            except Exception as e:
                print(f"Error: {e}")

output_file = "query_responses/results.csv"

with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    for company, count in ads_data.items():
        writer.writerow([company, count])
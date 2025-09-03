import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

ads_data = []

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file == "ads_viewed.json":
            try:
                with open(os.path.join(root, file), 'r') as f:
                    data = json.load(f)
                    for ad in data["impressions_history_ads_seen"]:
                        company_name = ad["string_map_data"]["Author"]["value"]
                        ads_data.append({"Company Name": company_name, "Number of Ads Viewed": 1})
            except Exception as e:
                print(f"Error processing {file}: {e}")

# Aggregate the data
aggregated_data = {}
for ad in ads_data:
    if ad["Company Name"] in aggregated_data:
        aggregated_data[ad["Company Name"]] += 1
    else:
        aggregated_data[ad["Company Name"]] = 1

# Write the data to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Company Name', 'Number of Ads Viewed']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for company, count in aggregated_data.items():
        writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})
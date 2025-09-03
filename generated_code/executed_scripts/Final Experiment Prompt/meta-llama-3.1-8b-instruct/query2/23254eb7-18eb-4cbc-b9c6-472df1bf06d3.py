import csv
import json

root_dir = "root_dir"

try:
    with open(f"{root_dir}/ads_information/ads_and_topics/ads_viewed.json", "r") as f:
        ads_viewed_data = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

company_ads_count = {}

for entry in ads_viewed_data.get("impressions_history_ads_seen", []):
    string_map_data = entry.get("string_map_data", {})
    author = string_map_data.get("Author", {}).get("value")
    if author is not None:
        if author not in company_ads_count:
            company_ads_count[author] = 0
        company_ads_count[author] += 1

with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    for company, count in company_ads_count.items():
        writer.writerow([company, count])
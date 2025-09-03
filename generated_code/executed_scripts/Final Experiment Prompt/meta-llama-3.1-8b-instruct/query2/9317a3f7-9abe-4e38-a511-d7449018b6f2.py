import csv
import json

root_dir = "root_dir"

try:
    with open(f"{root_dir}/ads_information/ads_and_topics/ads_viewed.json", "r") as f:
        ads_viewed_data = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")

try:
    with open(f"{root_dir}/ads_information/ads_and_topics/impressions_history_ads_seen.json", "r") as f:
        impressions_history_ads_seen_data = json.load(f)
except FileNotFoundError:
    impressions_history_ads_seen_data = {}  # Initialize an empty dictionary if the file does not exist

company_ads_count = {}

if "impressions_history_ads_seen" in impressions_history_ads_seen_data:
    for impression in impressions_history_ads_seen_data["impressions_history_ads_seen"]:
        author = impression.get("string_map_data", {}).get("Author", {}).get("value")
        if author:
            if author not in company_ads_count:
                company_ads_count[author] = 0
            company_ads_count[author] += 1

with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    for company, count in company_ads_count.items():
        writer.writerow([company, count])
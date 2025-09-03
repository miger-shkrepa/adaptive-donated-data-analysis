import os
import json
import csv

def process_ads_viewed(root_dir):
    ads_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')
    advertisers_path = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'advertisers_using_your_activity_or_information.json')

    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    ads_viewed_data = []
    advertisers_data = []

    try:
        with open(ads_viewed_path, 'r') as file:
            ads_viewed_data = json.load(file)
    except FileNotFoundError:
        ads_viewed_data = {"impressions_history_ads_seen": []}
    except json.JSONDecodeError:
        raise ValueError("Error: The ads_viewed.json file is not a valid JSON.")

    try:
        with open(advertisers_path, 'r') as file:
            advertisers_data = json.load(file)
    except FileNotFoundError:
        advertisers_data = {"ig_custom_audiences_all_types": []}
    except json.JSONDecodeError:
        raise ValueError("Error: The advertisers_using_your_activity_or_information.json file is not a valid JSON.")

    ads_count = {}

    for ad in ads_viewed_data.get("impressions_history_ads_seen", []):
        author = ad.get("string_map_data", {}).get("Author", {}).get("value", "")
        if author:
            ads_count[author] = ads_count.get(author, 0) + 1

    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Company Name', 'Number of Ads Viewed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for company, count in ads_count.items():
            writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})

if __name__ == "__main__":
    root_dir = "root_dir"
    process_ads_viewed(root_dir)
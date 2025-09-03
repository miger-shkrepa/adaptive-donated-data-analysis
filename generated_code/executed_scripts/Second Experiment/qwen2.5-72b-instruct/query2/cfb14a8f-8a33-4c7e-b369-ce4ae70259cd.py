import os
import json
import csv

root_dir = "root_dir"

def count_ads_viewed(root_dir):
    ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
    company_ads_count = {}

    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    if os.path.exists(ads_viewed_path):
        try:
            with open(ads_viewed_path, 'r') as file:
                data = json.load(file)
                ads_data = data.get("impressions_history_ads_seen", [])
                for ad in ads_data:
                    author = ad.get("string_map_data", {}).get("Author", {}).get("value")
                    if author:
                        company_ads_count[author] = company_ads_count.get(author, 0) + 1
        except json.JSONDecodeError:
            raise ValueError("Error: Failed to decode JSON from ads_viewed.json.")
    else:
        print("Warning: ads_viewed.json not found. Proceeding with empty data.")

    return company_ads_count

def write_to_csv(company_ads_count):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['Company Name', 'Number of Ads Viewed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for company, count in company_ads_count.items():
            writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})

try:
    company_ads_count = count_ads_viewed(root_dir)
    write_to_csv(company_ads_count)
except Exception as e:
    print(f"An error occurred: {e}")
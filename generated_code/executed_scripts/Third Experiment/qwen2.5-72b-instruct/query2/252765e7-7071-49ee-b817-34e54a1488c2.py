import os
import json
import csv

root_dir = "root_dir"

def count_ads_viewed(root):
    ads_viewed_path = os.path.join(root, "ads_information", "ads_and_topics", "ads_viewed.json")
    if not os.path.exists(ads_viewed_path):
        return {}
    
    try:
        with open(ads_viewed_path, 'r') as file:
            data = json.load(file)
            ads_viewed = data.get("impressions_history_ads_seen", [])
            ads_count = {}
            for ad in ads_viewed:
                string_map_data = ad.get("string_map_data", {})
                author = string_map_data.get("Author", {}).get("value")
                if author:
                    ads_count[author] = ads_count.get(author, 0) + 1
            return ads_count
    except Exception as e:
        raise ValueError(f"Error: Failed to process ads_viewed.json - {str(e)}")

def write_to_csv(data):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['Company Name', 'Number of Ads Viewed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for company, count in data.items():
            writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

try:
    ads_viewed_counts = count_ads_viewed(root_dir)
    write_to_csv(ads_viewed_counts)
except Exception as e:
    print(f"Error: {str(e)}")
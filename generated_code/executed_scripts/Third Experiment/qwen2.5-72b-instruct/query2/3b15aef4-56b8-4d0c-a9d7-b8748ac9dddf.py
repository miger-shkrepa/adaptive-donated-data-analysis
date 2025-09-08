import os
import json
import csv

root_dir = "root_dir"

def process_ads_data(root_dir):
    ads_data = {}
    try:
        ads_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
        if not os.path.exists(ads_path):
            raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")
        
        with open(ads_path, 'r') as file:
            data = json.load(file)
            for ad in data.get("impressions_history_ads_seen", []):
                author = ad.get("string_map_data", {}).get("Author", {}).get("value")
                if author:
                    ads_data[author] = ads_data.get(author, 0) + 1
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

    return ads_data

def write_to_csv(data, file_path):
    try:
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['Company Name', 'Number of Ads Viewed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for company, count in data.items():
                writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

if __name__ == "__main__":
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        ads_data = process_ads_data(root_dir)
        write_to_csv(ads_data, 'query_responses/results.csv')
    except Exception as e:
        print(e)
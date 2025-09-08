import os
import json
import csv

root_dir = "root_dir"

def process_ads_data(root_dir):
    ads_data = {}
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        ads_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
        if not os.path.exists(ads_path):
            return ads_data  # Return empty dict if the file is not found
        
        with open(ads_path, 'r') as file:
            data = json.load(file)
            for entry in data.get("impressions_history_ads_seen", []):
                author = entry.get("string_map_data", {}).get("Author", {}).get("value")
                if author:
                    ads_data[author] = ads_data.get(author, 0) + 1
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON data.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")
    
    return ads_data

def write_to_csv(data):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['Company Name', 'Number of Ads Viewed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for company, count in data.items():
            writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})

try:
    ads_data = process_ads_data(root_dir)
    write_to_csv(ads_data)
except Exception as e:
    print(e)
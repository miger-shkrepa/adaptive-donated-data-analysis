import os
import csv
import json

root_dir = "root_dir"

def get_ads_viewed_count(root_directory):
    ads_viewed_path = os.path.join(root_directory, "ads_information", "ads_and_topics", "ads_viewed.json")
    
    if not os.path.exists(root_directory):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.exists(ads_viewed_path):
        raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")
    
    try:
        with open(ads_viewed_path, 'r', encoding='utf-8') as file:
            ads_data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError("ValueError: The ads_viewed.json file is not a valid JSON file.")
    
    ads_viewed_count = len(ads_data.get("impressions_history_ads_seen", []))
    
    return ads_viewed_count

def write_csv(ads_viewed_count):
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Company Name", "Number of Ads Viewed"])
        csvwriter.writerow(["", ads_viewed_count])

try:
    ads_viewed_count = get_ads_viewed_count(root_dir)
    write_csv(ads_viewed_count)
except (FileNotFoundError, ValueError) as e:
    print(e)
    write_csv(0)  # Write an empty CSV with headers if there's an error
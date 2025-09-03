import os
import csv
import json

root_dir = "root_dir"

def get_ads_viewed_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data.get('impressions_history_ads_seen', [])
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The ads_viewed.json file is not a valid JSON file.")

def process_ads_data(ads_data):
    company_ads_count = {}
    for entry in ads_data:
        string_map_data = entry.get('string_map_data', {})
        author = string_map_data.get('Author', {}).get('value', 'Unknown Company')
        if author not in company_ads_count:
            company_ads_count[author] = 0
        company_ads_count[author] += 1
    return company_ads_count

def main():
    ads_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')
    
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.exists(ads_viewed_path):
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name', 'Number of Ads Viewed'])
        return

    ads_data = get_ads_viewed_data(ads_viewed_path)
    company_ads_count = process_ads_data(ads_data)

    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Company Name', 'Number of Ads Viewed'])
        for company, count in company_ads_count.items():
            writer.writerow([company, count])

if __name__ == "__main__":
    main()
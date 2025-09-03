import os
import csv
import json

root_dir = "root_dir"

def get_ads_viewed_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get('impressions_history_ads_seen', [])
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The ads_viewed.json file is not a valid JSON file.")

def aggregate_ads_data(root_directory):
    ads_viewed_path = os.path.join(root_directory, 'ads_information', 'ads_and_topics', 'ads_viewed.json')
    
    if not os.path.exists(root_directory):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.exists(ads_viewed_path):
        return {}

    ads_viewed_data = get_ads_viewed_data(ads_viewed_path)
    ads_count_by_company = {}

    for entry in ads_viewed_data:
        string_map_data = entry.get('string_map_data', {})
        author = string_map_data.get('Author', {}).get('value', 'Unknown Company')
        ads_count_by_company[author] = ads_count_by_company.get(author, 0) + 1

    return ads_count_by_company

def save_to_csv(data, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name', 'Number of Ads Viewed'])
            for company, count in data.items():
                writer.writerow([company, count])
    except IOError:
        raise IOError("IOError: Failed to write to the CSV file.")

def main():
    try:
        ads_data = aggregate_ads_data(root_dir)
        save_to_csv(ads_data, 'query_responses/results.csv')
    except Exception as e:
        print(e)
        save_to_csv({}, 'query_responses/results.csv')

if __name__ == "__main__":
    main()
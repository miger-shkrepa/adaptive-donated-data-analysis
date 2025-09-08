import os
import csv
import json

root_dir = "root_dir"

def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

def get_ads_viewed_data(root_directory):
    ads_viewed_path = os.path.join(root_directory, 'ads_information', 'ads_and_topics', 'ads_viewed.json')
    if not os.path.exists(ads_viewed_path):
        return {}

    ads_data = read_json_file(ads_viewed_path)
    ads_viewed = {}

    for entry in ads_data.get('impressions_history_ads_seen', []):
        author = entry.get('string_map_data', {}).get('Author', {}).get('value', 'Unknown')
        if author not in ads_viewed:
            ads_viewed[author] = 0
        ads_viewed[author] += 1

    return ads_viewed

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    ads_viewed_data = get_ads_viewed_data(root_dir)

    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Company Name', 'Number of Ads Viewed'])
        for company, count in ads_viewed_data.items():
            writer.writerow([company, count])

if __name__ == "__main__":
    main()
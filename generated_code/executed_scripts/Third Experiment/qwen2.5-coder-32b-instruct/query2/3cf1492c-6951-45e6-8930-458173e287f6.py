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

def get_advertisers_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data.get('ig_custom_audiences_all_types', [])
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The advertisers_using_your_activity_or_information.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The advertisers_using_your_activity_or_information.json file is not a valid JSON file.")

def main():
    ads_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')
    advertisers_path = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'advertisers_using_your_activity_or_information.json')

    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    ads_viewed_data = get_ads_viewed_data(ads_viewed_path) if os.path.exists(ads_viewed_path) else []
    advertisers_data = get_advertisers_data(advertisers_path) if os.path.exists(advertisers_path) else []

    advertiser_ads_count = {}

    for advertiser in advertisers_data:
        advertiser_name = advertiser.get('advertiser_name', 'Unknown')
        advertiser_ads_count[advertiser_name] = 0

    for ad in ads_viewed_data:
        for advertiser in advertisers_data:
            if advertiser.get('has_data_file_custom_audience') or advertiser.get('has_in_person_store_visit') or advertiser.get('has_remarketing_custom_audience'):
                advertiser_name = advertiser.get('advertiser_name', 'Unknown')
                advertiser_ads_count[advertiser_name] += 1

    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Company Name', 'Number of Ads Viewed'])
        for advertiser, count in advertiser_ads_count.items():
            writer.writerow([advertiser, count])

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name', 'Number of Ads Viewed'])
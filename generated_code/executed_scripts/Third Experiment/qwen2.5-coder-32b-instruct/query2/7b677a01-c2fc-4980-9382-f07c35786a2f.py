import os
import csv
import json

root_dir = "root_dir"

def get_ads_viewed_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data['impressions_history_ads_seen']
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The ads_viewed.json file is not a valid JSON file.")
    except KeyError:
        raise ValueError("ValueError: The ads_viewed.json file does not contain the expected structure.")

def get_ads_about_meta_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data['label_values']
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The ads_about_meta.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The ads_about_meta.json file is not a valid JSON file.")
    except KeyError:
        raise ValueError("ValueError: The ads_about_meta.json file does not contain the expected structure.")

def main():
    ads_viewed_file_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')
    ads_about_meta_file_path = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'ads_about_meta.json')

    ads_viewed_data = []
    ads_about_meta_data = []

    if os.path.exists(ads_viewed_file_path):
        ads_viewed_data = get_ads_viewed_data(ads_viewed_file_path)
    else:
        print("Warning: ads_viewed.json file is missing. The number of ads viewed will be treated as 0.")

    if os.path.exists(ads_about_meta_file_path):
        ads_about_meta_data = get_ads_about_meta_data(ads_about_meta_file_path)
    else:
        print("Warning: ads_about_meta.json file is missing. The company names will be treated as unavailable.")

    company_ads_count = {}

    for ad in ads_viewed_data:
        author = ad['string_map_data']['Author']['value']
        if author in company_ads_count:
            company_ads_count[author] += 1
        else:
            company_ads_count[author] = 1

    for label_value in ads_about_meta_data:
        if 'label' in label_value and label_value['label'] == 'Advertiser':
            advertiser = label_value['value']
            if advertiser not in company_ads_count:
                company_ads_count[advertiser] = 0

    output_file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    with open(output_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Company Name', 'Number of Ads Viewed'])
        for company, count in company_ads_count.items():
            writer.writerow([company, count])

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
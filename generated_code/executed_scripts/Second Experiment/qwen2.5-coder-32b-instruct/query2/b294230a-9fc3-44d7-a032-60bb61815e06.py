import os
import csv
import json

root_dir = "root_dir"

def get_ads_viewed_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            ads_viewed = data.get('impressions_history_ads_seen', [])
            return ads_viewed
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The ads_viewed.json file is not a valid JSON file.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while processing ads_viewed.json: {str(e)}")

def get_ads_about_meta_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            label_values = data.get('label_values', [])
            return label_values
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The ads_about_meta.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The ads_about_meta.json file is not a valid JSON file.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while processing ads_about_meta.json: {str(e)}")

def main():
    ads_viewed_file = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')
    ads_about_meta_file = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'ads_about_meta.json')

    ads_viewed_data = []
    ads_about_meta_data = []

    if os.path.exists(ads_viewed_file):
        ads_viewed_data = get_ads_viewed_data(ads_viewed_file)
    else:
        print("Warning: ads_viewed.json file is missing. Continuing with available data.")

    if os.path.exists(ads_about_meta_file):
        ads_about_meta_data = get_ads_about_meta_data(ads_about_meta_file)
    else:
        print("Warning: ads_about_meta.json file is missing. Continuing with available data.")

    company_ads_count = {}

    for ad in ads_viewed_data:
        author = ad.get('string_map_data', {}).get('Author', {}).get('value')
        if author:
            company_ads_count[author] = company_ads_count.get(author, 0) + 1

    for label_value in ads_about_meta_data:
        label = label_value.get('label')
        if label and label.startswith('Advertised by'):
            company_name = label.split('Advertised by ')[1]
            company_ads_count[company_name] = company_ads_count.get(company_name, 0)

    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Company Name', 'Number of Ads Viewed'])
        for company, count in company_ads_count.items():
            writer.writerow([company, count])

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Company Name', 'Number of Ads Viewed'])
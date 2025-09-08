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

def get_ads_viewed_data(root_dir):
    ads_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')
    if not os.path.exists(ads_viewed_path):
        return 0
    ads_viewed_data = read_json_file(ads_viewed_path)
    return len(ads_viewed_data.get('impressions_history_ads_seen', []))

def get_ads_about_meta_data(root_dir):
    ads_about_meta_path = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'ads_about_meta.json')
    if not os.path.exists(ads_about_meta_path):
        return {}
    ads_about_meta_data = read_json_file(ads_about_meta_path)
    label_values = ads_about_meta_data.get('label_values', [])
    company_info = {}
    for item in label_values:
        if 'label' in item and 'value' in item:
            if item['label'] == 'Advertiser':
                company_name = item['value']
                company_info[company_name] = company_info.get(company_name, 0) + 1
    return company_info

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    ads_viewed_count = get_ads_viewed_data(root_dir)
    company_ads_info = get_ads_about_meta_data(root_dir)
    
    if not os.path.exists('query_responses'):
        os.makedirs('query_responses')
    
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Company Name', 'Number of Ads Viewed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for company, count in company_ads_info.items():
            writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})
        
        # If no company data is found, write a row with 0 ads viewed
        if not company_ads_info:
            writer.writerow({'Company Name': '', 'Number of Ads Viewed': ads_viewed_count})
        else:
            # Adjust the count for each company based on total ads viewed
            total_ads = sum(company_ads_info.values())
            if total_ads < ads_viewed_count:
                writer.writerow({'Company Name': 'Other', 'Number of Ads Viewed': ads_viewed_count - total_ads})

if __name__ == "__main__":
    main()
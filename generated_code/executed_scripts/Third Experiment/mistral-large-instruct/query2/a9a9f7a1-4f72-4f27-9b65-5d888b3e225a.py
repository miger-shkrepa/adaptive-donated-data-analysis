import os
import json
import csv

def process_ads_viewed(root_dir):
    ads_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')

    if not os.path.exists(ads_viewed_path):
        raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")

    try:
        with open(ads_viewed_path, 'r') as file:
            ads_data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError("ValueError: The ads_viewed.json file is not a valid JSON.")

    company_ads_count = {}

    for ad in ads_data.get('impressions_history_ads_seen', []):
        author = ad.get('string_map_data', {}).get('Author', {}).get('value', 'Unknown')
        if author not in company_ads_count:
            company_ads_count[author] = 0
        company_ads_count[author] += 1

    return company_ads_count

def save_to_csv(data, output_path):
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Company Name', 'Number of Ads Viewed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for company, count in data.items():
            writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})

def main():
    root_dir = "root_dir"

    try:
        company_ads_count = process_ads_viewed(root_dir)
        save_to_csv(company_ads_count, 'query_responses/results.csv')
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
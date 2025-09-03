import os
import json
import csv

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def count_ads_viewed(root_dir):
    ads_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')
    company_ads_count = {}

    if not os.path.exists(ads_viewed_path):
        return company_ads_count

    try:
        ads_data = load_json_file(ads_viewed_path)
        ads_viewed = ads_data.get('impressions_history_ads_seen', [])

        for ad in ads_viewed:
            string_map_data = ad.get('string_map_data', [])
            for data in string_map_data:
                author = data.get('Author', {}).get('value')
                if author:
                    company_ads_count[author] = company_ads_count.get(author, 0) + 1

    except (FileNotFoundError, ValueError) as e:
        print(f"Error processing ads_viewed.json: {e}")
        return company_ads_count

    return company_ads_count

def write_to_csv(data, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Company Name', 'Number of Ads Viewed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for company, count in data.items():
                writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})
    except Exception as e:
        raise ValueError(f"Error: Failed to write to CSV file {output_path}. Reason: {e}")

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    try:
        company_ads_count = count_ads_viewed(root_dir)
        output_path = 'query_responses/results.csv'
        write_to_csv(company_ads_count, output_path)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
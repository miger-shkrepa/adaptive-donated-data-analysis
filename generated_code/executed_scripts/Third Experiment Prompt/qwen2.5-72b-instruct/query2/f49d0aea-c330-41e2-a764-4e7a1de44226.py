import os
import json
import csv

root_dir = "root_dir"

def load_json(file_path):
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

    try:
        if os.path.exists(ads_viewed_path):
            ads_data = load_json(ads_viewed_path)
            ads_viewed_list = ads_data.get('impressions_history_ads_seen', [])

            for entry in ads_viewed_list:
                string_map_data = entry.get('string_map_data', {})
                author = string_map_data.get('Author', {}).get('value')
                if author:
                    company_ads_count[author] = company_ads_count.get(author, 0) + 1
        else:
            print("Warning: ads_viewed.json does not exist. Assuming 0 ads viewed.")
    except Exception as e:
        print(f"Error processing ads_viewed.json: {e}")

    return company_ads_count

def save_to_csv(data, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Company Name', 'Number of Ads Viewed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for company, count in data.items():
                writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})
    except Exception as e:
        raise ValueError(f"Error: Failed to write CSV file. Reason: {e}")

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    try:
        company_ads_count = count_ads_viewed(root_dir)
        save_to_csv(company_ads_count, 'query_responses/results.csv')
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
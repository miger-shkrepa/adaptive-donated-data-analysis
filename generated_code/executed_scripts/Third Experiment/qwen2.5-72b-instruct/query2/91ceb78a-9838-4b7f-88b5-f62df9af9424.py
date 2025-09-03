import os
import json
import csv

root_dir = "root_dir"

def process_ads_viewed(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            ads_viewed = data.get("impressions_history_ads_seen", [])
            return ads_viewed
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

def count_ads_viewed_by_company(ads_viewed):
    company_ads_count = {}
    for entry in ads_viewed:
        string_map_data = entry.get("string_map_data", {})
        author = string_map_data.get("Author", {}).get("value")
        if author:
            company_ads_count[author] = company_ads_count.get(author, 0) + 1
    return company_ads_count

def generate_csv(company_ads_count):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Company Name', 'Number of Ads Viewed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for company, count in company_ads_count.items():
            writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})

def main():
    try:
        ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")
        if not os.path.exists(ads_viewed_path):
            generate_csv({})
            return

        ads_viewed = process_ads_viewed(ads_viewed_path)
        company_ads_count = count_ads_viewed_by_company(ads_viewed)
        generate_csv(company_ads_count)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
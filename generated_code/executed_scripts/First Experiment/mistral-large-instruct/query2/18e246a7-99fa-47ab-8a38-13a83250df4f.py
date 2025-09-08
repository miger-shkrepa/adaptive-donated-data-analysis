import os
import json
import csv

root_dir = "root_dir"

def process_ads_viewed(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            ads_seen = data.get("impressions_history_ads_seen", [])
            return ads_seen
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The file is not a valid JSON.")

def count_ads_by_company(ads_seen):
    company_ads_count = {}
    for ad in ads_seen:
        author = ad.get("string_map_data", {}).get("Author", {}).get("value", "Unknown")
        if author in company_ads_count:
            company_ads_count[author] += 1
        else:
            company_ads_count[author] = 1
    return company_ads_count

def save_to_csv(data, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
            fieldnames = ['Company Name', 'Number of Ads Viewed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for company, count in data.items():
                writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})
    except Exception as e:
        raise ValueError(f"ValueError: Failed to write to CSV. {str(e)}")

def main():
    ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    ads_seen = process_ads_viewed(ads_viewed_path)
    company_ads_count = count_ads_by_company(ads_seen)
    output_path = 'query_responses/results.csv'
    save_to_csv(company_ads_count, output_path)

if __name__ == "__main__":
    main()
import os
import json
import csv

root_dir = "root_dir"

def get_ads_viewed(root_dir):
    try:
        ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
        if not os.path.exists(ads_viewed_path):
            return []
        
        with open(ads_viewed_path, 'r') as file:
            ads_viewed_data = json.load(file)
            return ads_viewed_data.get('impressions_history_ads_seen', [])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def get_company_names(ads_viewed_data):
    company_names = {}
    for ad in ads_viewed_data:
        string_map_data = ad.get('string_map_data', {})
        author = string_map_data.get('Author', {}).get('value', '')
        if author:
            if author not in company_names:
                company_names[author] = 1
            else:
                company_names[author] += 1
    return company_names

def write_to_csv(company_names):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            for company, count in company_names.items():
                writer.writerow([company, count])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        ads_viewed_data = get_ads_viewed(root_dir)
        company_names = get_company_names(ads_viewed_data)
        write_to_csv(company_names)
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
        raise FileNotFoundError("FileNotFoundError: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()
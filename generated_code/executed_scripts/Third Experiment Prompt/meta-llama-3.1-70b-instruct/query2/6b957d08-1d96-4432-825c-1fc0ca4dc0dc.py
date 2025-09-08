import os
import csv
import json

root_dir = "root_dir"

def get_ads_viewed(root_dir):
    try:
        ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
        if not os.path.exists(ads_viewed_path):
            raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")
        
        with open(ads_viewed_path, 'r') as file:
            ads_viewed_data = json.load(file)
            return ads_viewed_data
    except Exception as e:
        raise ValueError("Error: " + str(e))

def get_company_ads(ads_viewed_data):
    company_ads = {}
    for ad in ads_viewed_data.get("impressions_history_ads_seen", []):
        author = ad.get("string_map_data", {}).get("Author", {}).get("value")
        if author:
            if author not in company_ads:
                company_ads[author] = 0
            company_ads[author] += 1
    return company_ads

def write_to_csv(company_ads):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            for company, count in company_ads.items():
                writer.writerow([company, count])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        ads_viewed_data = get_ads_viewed(root_dir)
        company_ads = get_company_ads(ads_viewed_data)
        write_to_csv(company_ads)
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
        raise FileNotFoundError("FileNotFoundError: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()
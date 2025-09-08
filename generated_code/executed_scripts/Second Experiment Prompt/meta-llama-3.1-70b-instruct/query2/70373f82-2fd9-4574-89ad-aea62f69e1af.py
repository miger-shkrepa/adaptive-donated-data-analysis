import os
import csv
import json

root_dir = "root_dir"

def get_ads_viewed(root_dir):
    try:
        ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        if not os.path.exists(ads_viewed_path):
            return []
        
        with open(ads_viewed_path, 'r') as file:
            ads_viewed_data = json.load(file)
            ads_viewed = ads_viewed_data.get("impressions_history_ads_seen", [])
            return ads_viewed
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}") from e
    except Exception as e:
        raise ValueError(f"Error: {e}") from e

def get_company_ads(ads_viewed):
    company_ads = {}
    for ad in ads_viewed:
        author = ad.get("string_map_data", {}).get("Author", {}).get("value")
        if author:
            if author not in company_ads:
                company_ads[author] = 0
            company_ads[author] += 1
    return company_ads

def write_to_csv(company_ads):
    with open('query_responses/results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Company Name", "Number of Ads Viewed"])
        for company, ads_viewed in company_ads.items():
            writer.writerow([company, ads_viewed])

def main():
    try:
        ads_viewed = get_ads_viewed(root_dir)
        company_ads = get_company_ads(ads_viewed)
        write_to_csv(company_ads)
    
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
        raise FileNotFoundError(f"Error: {e}") from e
    except Exception as e:
        raise ValueError(f"Error: {e}") from e

if __name__ == "__main__":
    main()
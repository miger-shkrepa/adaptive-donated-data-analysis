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
    
    except Exception as e:
        raise Exception("Error: Unable to retrieve ads_viewed.json file. " + str(e))

def get_company_ads_viewed(ads_viewed):
    company_ads_viewed = {}
    for ad in ads_viewed:
        author = ad.get("string_map_data", {}).get("Author", {}).get("value")
        if author:
            if author in company_ads_viewed:
                company_ads_viewed[author] += 1
            else:
                company_ads_viewed[author] = 1
    return company_ads_viewed

def write_to_csv(company_ads_viewed):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            for company, count in company_ads_viewed.items():
                writer.writerow([company, count])
    
    except Exception as e:
        raise Exception("Error: Unable to write to CSV file. " + str(e))

def main():
    try:
        ads_viewed = get_ads_viewed(root_dir)
        if not ads_viewed:
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Company Name", "Number of Ads Viewed"])
            return
        
        company_ads_viewed = get_company_ads_viewed(ads_viewed)
        write_to_csv(company_ads_viewed)
    
    except Exception as e:
        raise Exception("Error: " + str(e))

if __name__ == "__main__":
    main()
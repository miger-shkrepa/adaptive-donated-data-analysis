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
            ads_viewed = ads_viewed_data.get("impressions_history_ads_seen", [])
            return ads_viewed
    
    except FileNotFoundError as e:
        raise FileNotFoundError("Error: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

def get_company_ads(ads_viewed):
    company_ads = {}
    for ad in ads_viewed:
        author = ad.get("string_map_data", {}).get("Author", {}).get("value", "")
        if author:
            if author in company_ads:
                company_ads[author] += 1
            else:
                company_ads[author] = 1
    return company_ads

def write_to_csv(company_ads):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            for company, ads_viewed in company_ads.items():
                writer.writerow([company, ads_viewed])
    
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        ads_viewed = get_ads_viewed(root_dir)
        if not ads_viewed:
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Company Name", "Number of Ads Viewed"])
            return
        
        company_ads = get_company_ads(ads_viewed)
        write_to_csv(company_ads)
    
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
        print("Error: " + str(e))
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()
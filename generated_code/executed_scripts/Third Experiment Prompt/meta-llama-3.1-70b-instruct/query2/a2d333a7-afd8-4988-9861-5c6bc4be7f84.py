import os
import json
import csv

root_dir = "root_dir"

def get_company_ads_viewed(root_dir):
    company_ads_viewed = {}
    try:
        ads_and_topics_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
        if not os.path.exists(ads_and_topics_dir):
            raise FileNotFoundError("FileNotFoundError: The ads_and_topics directory does not exist.")
        
        ads_viewed_file = os.path.join(ads_and_topics_dir, "ads_viewed.json")
        if not os.path.exists(ads_viewed_file):
            return company_ads_viewed
        
        with open(ads_viewed_file, 'r', encoding='utf-8') as file:
            ads_viewed_data = json.load(file)
            for ad in ads_viewed_data['impressions_history_ads_seen']:
                company_name = ad.get('string_map_data', {}).get('Company Name', {}).get('value')
                if company_name:
                    company_ads_viewed[company_name] = company_ads_viewed.get(company_name, 0) + 1
        
        advertisers_using_your_activity_file = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")
        if not os.path.exists(advertisers_using_your_activity_file):
            return company_ads_viewed
        
        with open(advertisers_using_your_activity_file, 'r', encoding='utf-8') as file:
            advertisers_data = json.load(file)
            for advertiser in advertisers_data['ig_custom_audiences_all_types']:
                company_name = advertiser.get('advertiser_name')
                if company_name:
                    company_ads_viewed[company_name] = company_ads_viewed.get(company_name, 0)
        
        return company_ads_viewed
    
    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_to_csv(company_ads_viewed):
    try:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            for company, ads_viewed in company_ads_viewed.items():
                writer.writerow([company, ads_viewed])
    
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        company_ads_viewed = get_company_ads_viewed(root_dir)
        write_to_csv(company_ads_viewed)
    
    except Exception as e:
        if "FileNotFoundError" in str(e):
            with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Company Name", "Number of Ads Viewed"])
        else:
            raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()
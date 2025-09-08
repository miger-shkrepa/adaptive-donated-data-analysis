import os
import csv
import json

root_dir = "root_dir"

def get_ads_viewed(root_dir):
    try:
        ads_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')
        if not os.path.exists(ads_viewed_path):
            raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")
        
        with open(ads_viewed_path, 'r') as file:
            ads_viewed_data = json.load(file)
            return ads_viewed_data['impressions_history_ads_seen']
    
    except FileNotFoundError as e:
        raise FileNotFoundError("Error: " + str(e))

def get_advertisers_using_your_activity(root_dir):
    try:
        advertisers_path = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'advertisers_using_your_activity_or_information.json')
        if not os.path.exists(advertisers_path):
            raise FileNotFoundError("FileNotFoundError: The advertisers_using_your_activity_or_information.json file does not exist.")
        
        with open(advertisers_path, 'r') as file:
            advertisers_data = json.load(file)
            return advertisers_data['ig_custom_audiences_all_types']
    
    except FileNotFoundError as e:
        raise FileNotFoundError("Error: " + str(e))

def get_company_name(advertiser):
    return advertiser['advertiser_name']

def get_number_of_ads_viewed(ads_viewed):
    return len(ads_viewed)

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        ads_viewed = get_ads_viewed(root_dir)
        advertisers = get_advertisers_using_your_activity(root_dir)
        
        company_names = [get_company_name(advertiser) for advertiser in advertisers]
        number_of_ads_viewed = [get_number_of_ads_viewed(ads_viewed) for _ in advertisers]
        
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            for company, number in zip(company_names, number_of_ads_viewed):
                writer.writerow([company, number])
    
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
        raise FileNotFoundError("Error: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()
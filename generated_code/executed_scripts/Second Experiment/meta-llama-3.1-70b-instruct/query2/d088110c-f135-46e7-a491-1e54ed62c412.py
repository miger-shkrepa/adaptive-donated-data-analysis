import os
import json
import csv

root_dir = "root_dir"

def get_ads_viewed(root_dir):
    try:
        ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
        if not os.path.exists(ads_viewed_path):
            raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")
        
        with open(ads_viewed_path, 'r') as f:
            ads_viewed_data = json.load(f)
            return ads_viewed_data["impressions_history_ads_seen"]
    except Exception as e:
        raise FileNotFoundError("Error: " + str(e))

def get_advertisers_using_your_activity_or_information(root_dir):
    try:
        advertisers_using_your_activity_or_information_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")
        if not os.path.exists(advertisers_using_your_activity_or_information_path):
            raise FileNotFoundError("FileNotFoundError: The advertisers_using_your_activity_or_information.json file does not exist.")
        
        with open(advertisers_using_your_activity_or_information_path, 'r') as f:
            advertisers_using_your_activity_or_information_data = json.load(f)
            return advertisers_using_your_activity_or_information_data["ig_custom_audiences_all_types"]
    except Exception as e:
        raise FileNotFoundError("Error: " + str(e))

def get_company_name(advertiser):
    return advertiser["advertiser_name"]

def get_number_of_ads_viewed(ads_viewed, company_name):
    count = 0
    for ad in ads_viewed:
        if "string_map_data" in ad and "Author" in ad["string_map_data"] and ad["string_map_data"]["Author"]["value"] == company_name:
            count += 1
    return count

def generate_csv(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        ads_viewed = get_ads_viewed(root_dir)
        advertisers_using_your_activity_or_information = get_advertisers_using_your_activity_or_information(root_dir)
        
        company_names = [get_company_name(advertiser) for advertiser in advertisers_using_your_activity_or_information]
        number_of_ads_viewed = [get_number_of_ads_viewed(ads_viewed, company_name) for company_name in company_names]
        
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Company Name', 'Number of Ads Viewed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for company_name, num_ads_viewed in zip(company_names, number_of_ads_viewed):
                writer.writerow({'Company Name': company_name, 'Number of Ads Viewed': num_ads_viewed})
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Company Name', 'Number of Ads Viewed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        raise FileNotFoundError("Error: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

generate_csv(root_dir)
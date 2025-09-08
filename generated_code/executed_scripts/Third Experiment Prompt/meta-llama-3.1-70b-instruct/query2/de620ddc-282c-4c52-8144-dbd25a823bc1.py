import os
import csv
import json

root_dir = "root_dir"

def get_ads_viewed(root_dir):
    try:
        ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
        if not os.path.exists(ads_viewed_path):
            return []
        
        with open(ads_viewed_path, 'r', encoding='utf-8') as file:
            ads_viewed_data = json.load(file)
            return ads_viewed_data.get('impressions_history_ads_seen', [])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def get_advertisers_using_your_activity(root_dir):
    try:
        advertisers_using_your_activity_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")
        if not os.path.exists(advertisers_using_your_activity_path):
            return []
        
        with open(advertisers_using_your_activity_path, 'r', encoding='utf-8') as file:
            advertisers_using_your_activity_data = json.load(file)
            return advertisers_using_your_activity_data.get('ig_custom_audiences_all_types', [])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def get_company_name(advertiser):
    return advertiser.get('advertiser_name', '')

def get_number_of_ads_viewed(ads_viewed):
    return len(ads_viewed)

def get_results(root_dir):
    try:
        ads_viewed = get_ads_viewed(root_dir)
        advertisers_using_your_activity = get_advertisers_using_your_activity(root_dir)
        
        results = []
        for advertiser in advertisers_using_your_activity:
            company_name = get_company_name(advertiser)
            number_of_ads_viewed = get_number_of_ads_viewed(ads_viewed)
            results.append([company_name, number_of_ads_viewed])
        
        return results
    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_results_to_csv(results):
    try:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            writer.writerows(results)
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        results = get_results(root_dir)
        if not results:
            results = []
        save_results_to_csv(results)
    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()
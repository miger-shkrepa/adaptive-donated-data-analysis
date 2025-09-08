import os
import json
import csv

root_dir = "root_dir"

def get_ads_viewed(root_dir):
    try:
        ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
        if not os.path.exists(ads_viewed_path):
            raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")
        with open(ads_viewed_path, 'r') as file:
            ads_viewed_data = json.load(file)
            return ads_viewed_data["impressions_history_ads_seen"]
    except Exception as e:
        raise FileNotFoundError("Error: " + str(e))

def get_advertisers_using_your_activity(root_dir):
    try:
        advertisers_using_your_activity_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity.json")
        if not os.path.exists(advertisers_using_your_activity_path):
            raise FileNotFoundError("FileNotFoundError: The advertisers_using_your_activity.json file does not exist.")
        with open(advertisers_using_your_activity_path, 'r') as file:
            advertisers_using_your_activity_data = json.load(file)
            return advertisers_using_your_activity_data["ig_custom_audiences_all_types"]
    except Exception as e:
        raise FileNotFoundError("Error: " + str(e))

def generate_csv(root_dir):
    try:
        company_ads_viewed = {}
        ads_viewed_data = get_ads_viewed(root_dir)
        for ad in ads_viewed_data:
            author = ad["string_map_data"]["Author"]["value"]
            if author not in company_ads_viewed:
                company_ads_viewed[author] = 1
            else:
                company_ads_viewed[author] += 1

        advertisers_using_your_activity_data = get_advertisers_using_your_activity(root_dir)
        for advertiser in advertisers_using_your_activity_data:
            advertiser_name = advertiser["advertiser_name"]
            if advertiser_name not in company_ads_viewed:
                company_ads_viewed[advertiser_name] = 0

        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            for company, ads_viewed in company_ads_viewed.items():
                writer.writerow([company, ads_viewed])
    except FileNotFoundError as e:
        if "ads_viewed.json" in str(e):
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Company Name", "Number of Ads Viewed"])
        else:
            raise FileNotFoundError("Error: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    if not os.path.exists('query_responses'):
        os.makedirs('query_responses')
    generate_csv(root_dir)
except FileNotFoundError as e:
    raise FileNotFoundError("FileNotFoundError: " + str(e))
except Exception as e:
    raise ValueError("Error: " + str(e))
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

def get_company_ads(root_dir):
    try:
        company_ads = {}
        ads_viewed_data = get_ads_viewed(root_dir)
        
        for ad in ads_viewed_data:
            author = ad["string_map_data"]["Author"]["value"]
            if author not in company_ads:
                company_ads[author] = 1
            else:
                company_ads[author] += 1
        
        return company_ads
    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_to_csv(root_dir):
    try:
        company_ads = get_company_ads(root_dir)
        
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            for company, ads_viewed in company_ads.items():
                writer.writerow([company, ads_viewed])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        if not os.path.exists('query_responses'):
            os.makedirs('query_responses')
        
        write_to_csv(root_dir)
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
        raise FileNotFoundError("Error: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main(root_dir)
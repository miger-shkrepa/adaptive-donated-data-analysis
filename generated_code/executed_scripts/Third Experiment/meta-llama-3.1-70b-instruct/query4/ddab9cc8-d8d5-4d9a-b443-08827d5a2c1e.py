import os
import csv

root_dir = "root_dir"

def get_companies_with_access(root_dir):
    companies = set()
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Check if ads_information directory exists
        ads_info_dir = os.path.join(root_dir, "ads_information")
        if not os.path.exists(ads_info_dir):
            return companies
        
        # Check if ads_and_topics directory exists
        ads_and_topics_dir = os.path.join(ads_info_dir, "ads_and_topics")
        if not os.path.exists(ads_and_topics_dir):
            return companies
        
        # Check if ads_viewed.json file exists
        ads_viewed_file = os.path.join(ads_and_topics_dir, "ads_viewed.json")
        if os.path.exists(ads_viewed_file):
            with open(ads_viewed_file, 'r') as file:
                # Assuming the JSON file has the same structure as in the directory structure
                import json
                data = json.load(file)
                for ad in data["impressions_history_ads_seen"]:
                    if "string_map_data" in ad and "Author" in ad["string_map_data"]:
                        companies.add(ad["string_map_data"]["Author"]["value"])
        
        # Check if instagram_ads_and_businesses directory exists
        instagram_ads_dir = os.path.join(ads_info_dir, "instagram_ads_and_businesses")
        if not os.path.exists(instagram_ads_dir):
            return companies
        
        # Check if subscription_for_no_ads.json file exists
        subscription_file = os.path.join(instagram_ads_dir, "subscription_for_no_ads.json")
        if os.path.exists(subscription_file):
            with open(subscription_file, 'r') as file:
                # Assuming the JSON file has the same structure as in the directory structure
                import json
                data = json.load(file)
                for label in data["label_values"]:
                    companies.add(label["label"])
        
        return companies
    
    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(companies):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name"])
            for company in companies:
                writer.writerow([company])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    companies = get_companies_with_access(root_dir)
    if not companies:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name"])
    else:
        save_to_csv(companies)

if __name__ == "__main__":
    main()
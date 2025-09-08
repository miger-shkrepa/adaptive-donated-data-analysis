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
        raise FileNotFoundError(f"Error: {e}")

def get_ads_and_topics(root_dir):
    try:
        ads_and_topics_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "accounts_you're_not_interested_in.json")
        if not os.path.exists(ads_and_topics_path):
            raise FileNotFoundError("FileNotFoundError: The accounts_you're_not_interested_in.json file does not exist.")
        
        with open(ads_and_topics_path, 'r') as file:
            ads_and_topics_data = json.load(file)
            ads_and_topics = ads_and_topics_data.get("impressions_history_recs_hidden_authors", [])
            return ads_and_topics
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")

def get_company_ads_viewed(ads_viewed, ads_and_topics):
    company_ads_viewed = {}
    for ad in ads_viewed:
        author = ad.get("string_map_data", {}).get("Author", {}).get("value")
        if author:
            if author not in company_ads_viewed:
                company_ads_viewed[author] = 1
            else:
                company_ads_viewed[author] += 1
    
    for topic in ads_and_topics:
        author = topic.get("string_map_data", {}).get("Benutzername", {}).get("value")
        if author:
            if author not in company_ads_viewed:
                company_ads_viewed[author] = 0
    
    return company_ads_viewed

def write_to_csv(company_ads_viewed):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            for company, ads_viewed in company_ads_viewed.items():
                writer.writerow([company, ads_viewed])
    
    except Exception as e:
        raise Exception(f"Error: Unable to write to CSV file. {e}")

def main():
    try:
        ads_viewed = get_ads_viewed(root_dir)
        ads_and_topics = get_ads_and_topics(root_dir)
        company_ads_viewed = get_company_ads_viewed(ads_viewed, ads_and_topics)
        write_to_csv(company_ads_viewed)
    
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
        print(f"Error: {e}")
    
    except Exception as e:
        raise Exception(f"Error: {e}")

if __name__ == "__main__":
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    main()
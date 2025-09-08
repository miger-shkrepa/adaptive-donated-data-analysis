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
        raise ValueError("Error: " + str(e))

def get_company_ads_viewed(ads_viewed_data):
    company_ads_viewed = {}
    for ad in ads_viewed_data:
        author = ad["string_map_data"]["Author"]["value"]
        if author not in company_ads_viewed:
            company_ads_viewed[author] = 1
        else:
            company_ads_viewed[author] += 1
    return company_ads_viewed

def write_to_csv(company_ads_viewed):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
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
        
        ads_viewed_data = get_ads_viewed(root_dir)
        company_ads_viewed = get_company_ads_viewed(ads_viewed_data)
        write_to_csv(company_ads_viewed)
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
        raise FileNotFoundError("FileNotFoundError: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()
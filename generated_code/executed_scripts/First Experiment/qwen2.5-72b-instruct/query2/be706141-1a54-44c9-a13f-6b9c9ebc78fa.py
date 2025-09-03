import os
import json
import csv

root_dir = "root_dir"

def count_ads_viewed(root_directory):
    ads_viewed_path = os.path.join(root_directory, "ads_information", "ads_and_topics", "ads_viewed.json")
    company_ads_count = {}

    try:
        if not os.path.exists(root_directory):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        if not os.path.exists(ads_viewed_path):
            raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")
        
        with open(ads_viewed_path, 'r') as file:
            data = json.load(file)
            ads_data = data.get("ads_viewed.json", {}).get("structure", {}).get("impressions_history_ads_seen", [])
            
            for ad in ads_data:
                author = ad.get("string_map_data", {}).get("Author", {}).get("value")
                if author:
                    if author in company_ads_count:
                        company_ads_count[author] += 1
                    else:
                        company_ads_count[author] = 1

        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name', 'Number of Ads Viewed'])
            for company, count in company_ads_count.items():
                writer.writerow([company, count])

    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {str(e)}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {str(e)}")

try:
    count_ads_viewed(root_dir)
except Exception as e:
    print(str(e))
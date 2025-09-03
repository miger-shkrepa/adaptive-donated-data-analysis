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
        raise FileNotFoundError("Error: " + str(e))
    except json.JSONDecodeError as e:
        raise ValueError("Error: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

def get_company_names(ads_viewed):
    company_names = {}
    for ad in ads_viewed:
        string_map_data = ad.get("string_map_data", {})
        author = string_map_data.get("Author", {}).get("value", "")
        if author:
            if author in company_names:
                company_names[author] += 1
            else:
                company_names[author] = 1
    return company_names

def write_to_csv(company_names):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            for company, count in company_names.items():
                writer.writerow([company, count])
    
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        ads_viewed = get_ads_viewed(root_dir)
        if not ads_viewed:
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Company Name", "Number of Ads Viewed"])
            return
        
        company_names = get_company_names(ads_viewed)
        write_to_csv(company_names)
    
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()
import os
import json
import csv

root_dir = "root_dir"

def get_ads_viewed(root_dir):
    try:
        ads_and_topics_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
        if not os.path.exists(ads_and_topics_dir):
            raise FileNotFoundError("FileNotFoundError: The ads_and_topics directory does not exist.")
        
        ads_viewed_file = os.path.join(ads_and_topics_dir, "ads_viewed.json")
        if not os.path.exists(ads_viewed_file):
            raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")
        
        with open(ads_viewed_file, "r") as file:
            ads_viewed_data = json.load(file)
        
        return ads_viewed_data
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: {e}")

def get_company_ads_viewed(ads_viewed_data):
    company_ads_viewed = {}
    
    for impression in ads_viewed_data["impressions_history_ads_seen"]:
        if "string_map_data" in impression:
            string_map_data = impression["string_map_data"]
            if "Author" in string_map_data:
                company = string_map_data["Author"]["value"]
                if company not in company_ads_viewed:
                    company_ads_viewed[company] = 1
                else:
                    company_ads_viewed[company] += 1
    
    return company_ads_viewed

def write_to_csv(company_ads_viewed):
    try:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            for company, ads_viewed in company_ads_viewed.items():
                writer.writerow([company, ads_viewed])
    
    except Exception as e:
        raise Exception(f"Error: {e}")

def main():
    try:
        ads_viewed_data = get_ads_viewed(root_dir)
        company_ads_viewed = get_company_ads_viewed(ads_viewed_data)
        write_to_csv(company_ads_viewed)
    
    except Exception as e:
        print(f"Error: {e}")
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])

if __name__ == "__main__":
    main()
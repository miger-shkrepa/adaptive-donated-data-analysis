import os
import json
import csv

root_dir = "root_dir"

def get_ads_viewed(root_dir):
    try:
        ads_info_dir = os.path.join(root_dir, "ads_information")
        if not os.path.exists(ads_info_dir):
            raise FileNotFoundError("FileNotFoundError: The ads information directory does not exist.")
        
        ads_and_topics_dir = os.path.join(ads_info_dir, "ads_and_topics")
        if not os.path.exists(ads_and_topics_dir):
            raise FileNotFoundError("FileNotFoundError: The ads and topics directory does not exist.")
        
        ads_viewed_file = os.path.join(ads_and_topics_dir, "ads_viewed.json")
        if not os.path.exists(ads_viewed_file):
            raise FileNotFoundError("FileNotFoundError: The ads viewed file does not exist.")
        
        with open(ads_viewed_file, "r") as file:
            ads_viewed_data = json.load(file)
        
        return ads_viewed_data
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")
    
    except Exception as e:
        raise ValueError(f"Error: {e}")

def get_company_ads(ads_viewed_data):
    company_ads = {}
    
    for ad in ads_viewed_data["impressions_history_ads_seen"]:
        if "string_map_data" in ad:
            if "Author" in ad["string_map_data"]:
                company = ad["string_map_data"]["Author"]["value"]
                if company not in company_ads:
                    company_ads[company] = 1
                else:
                    company_ads[company] += 1
    
    return company_ads

def write_to_csv(company_ads):
    try:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            for company, ads in company_ads.items():
                writer.writerow([company, ads])
    
    except Exception as e:
        raise ValueError(f"Error: {e}")

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        ads_viewed_data = get_ads_viewed(root_dir)
        company_ads = get_company_ads(ads_viewed_data)
        write_to_csv(company_ads)
    
    except FileNotFoundError as e:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
        raise FileNotFoundError(f"Error: {e}")
    
    except Exception as e:
        raise ValueError(f"Error: {e}")

if __name__ == "__main__":
    main()
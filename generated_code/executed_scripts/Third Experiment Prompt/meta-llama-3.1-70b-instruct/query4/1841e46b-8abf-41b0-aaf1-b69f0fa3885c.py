import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access(root_dir):
    companies = set()
    try:
        ads_and_businesses_dir = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses")
        if not os.path.exists(ads_and_businesses_dir):
            raise FileNotFoundError("FileNotFoundError: The 'instagram_ads_and_businesses' directory does not exist.")
        
        advertisers_file = os.path.join(ads_and_businesses_dir, "advertisers_using_your_activity_or_information.json")
        if not os.path.exists(advertisers_file):
            return companies
        
        with open(advertisers_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for advertiser in data.get("ig_custom_audiences_all_types", []):
                companies.add(advertiser.get("advertiser_name", ""))
        
        return companies
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

def write_to_csv(companies):
    with open("query_responses/results.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name"])
        for company in companies:
            writer.writerow([company])

if __name__ == "__main__":
    companies = get_companies_with_access(root_dir)
    write_to_csv(companies)
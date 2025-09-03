import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access(root_dir):
    companies = set()
    advertisers_file = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")
    
    if os.path.exists(advertisers_file):
        with open(advertisers_file, "r") as f:
            data = json.load(f)
            for advertiser in data["ig_custom_audiences_all_types"]:
                companies.add(advertiser["advertiser_name"])
    else:
        raise FileNotFoundError("Error: The file 'advertisers_using_your_activity_or_information.json' does not exist.")
    
    return companies

def write_to_csv(companies):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name"])
        for company in companies:
            writer.writerow([company])

try:
    companies = get_companies_with_access(root_dir)
    write_to_csv(companies)
except FileNotFoundError as e:
    raise FileNotFoundError(f"FileNotFoundError: {e}")
except Exception as e:
    raise ValueError(f"Error: {e}")
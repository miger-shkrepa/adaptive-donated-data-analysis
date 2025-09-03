import os
import csv
import json

root_dir = "root_dir"

def get_companies_with_access(root_dir):
    companies = set()
    try:
        ads_and_businesses_dir = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses")
        if not os.path.exists(ads_and_businesses_dir):
            raise FileNotFoundError("FileNotFoundError: The 'ads_information/instagram_ads_and_businesses' directory does not exist.")
        
        advertisers_file = os.path.join(ads_and_businesses_dir, "advertisers_using_your_activity_or_information.json")
        if not os.path.exists(advertisers_file):
            return companies
        
        with open(advertisers_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for advertiser in data.get("ig_custom_audiences_all_types", []):
                companies.add(advertiser.get("advertiser_name", ""))
        
        return companies
    
    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_companies_to_csv(companies):
    try:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name"])
            for company in companies:
                writer.writerow([company])
    
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        companies = get_companies_with_access(root_dir)
        write_companies_to_csv(companies)
    
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name"])
        print(e)
    
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
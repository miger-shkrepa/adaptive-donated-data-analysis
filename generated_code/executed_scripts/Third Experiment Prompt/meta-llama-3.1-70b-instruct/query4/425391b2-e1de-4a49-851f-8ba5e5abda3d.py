import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access(root_dir):
    companies = set()
    file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for advertiser in data["ig_custom_audiences_all_types"]:
                companies.add(advertiser["advertiser_name"])
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file 'advertisers_using_your_activity_or_information.json' does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file 'advertisers_using_your_activity_or_information.json' is not a valid JSON file.")
    
    return companies

def write_to_csv(companies):
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Company Name"])
        for company in companies:
            writer.writerow([company])

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        companies = get_companies_with_access(root_dir)
        write_to_csv(companies)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
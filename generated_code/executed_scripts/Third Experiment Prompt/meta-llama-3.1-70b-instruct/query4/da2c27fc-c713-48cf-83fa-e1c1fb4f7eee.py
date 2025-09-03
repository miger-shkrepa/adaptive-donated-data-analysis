import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access(root_dir):
    companies = []
    file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")
    
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for advertiser in data["ig_custom_audiences_all_types"]:
                companies.append(advertiser["advertiser_name"])
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file 'advertisers_using_your_activity_or_information.json' does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file 'advertisers_using_your_activity_or_information.json' is not a valid JSON file.")
    
    return companies

def save_to_csv(companies):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Company Name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for company in companies:
            writer.writerow({'Company Name': company})

def main():
    try:
        companies = get_companies_with_access(root_dir)
        save_to_csv(companies)
    except FileNotFoundError as e:
        print(e)
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Company Name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    except ValueError as e:
        print(e)
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Company Name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

if __name__ == "__main__":
    main()
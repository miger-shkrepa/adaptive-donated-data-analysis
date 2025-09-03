import os
import csv
import json

root_dir = "root_dir"

def get_companies_with_access(root_dir):
    companies = set()
    try:
        ads_and_businesses_dir = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses")
        if os.path.exists(ads_and_businesses_dir):
            advertisers_file = os.path.join(ads_and_businesses_dir, "advertisers_using_your_activity_or_information.json")
            if os.path.exists(advertisers_file):
                with open(advertisers_file, 'r') as file:
                    data = json.load(file)
                    for advertiser in data.get("ig_custom_audiences_all_types", []):
                        companies.add(advertiser.get("advertiser_name", ""))
        
        apps_and_websites_dir = os.path.join(root_dir, "apps_and_websites_off_of_instagram", "apps_and_websites")
        if os.path.exists(apps_and_websites_dir):
            activity_file = os.path.join(apps_and_websites_dir, "your_activity_off_meta_technologies_settings.json")
            if os.path.exists(activity_file):
                with open(activity_file, 'r') as file:
                    data = json.load(file)
                    for label in data.get("label_values", []):
                        if isinstance(label, dict) and "label" in label:
                            companies.add(label.get("label", ""))
        
    except Exception as e:
        raise ValueError(f"Error: {e}")
    
    return companies

def write_companies_to_csv(companies):
    with open('query_responses/results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Company Name"])
        for company in companies:
            writer.writerow([company])

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        companies = get_companies_with_access(root_dir)
        write_companies_to_csv(companies)
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name"])
        print(f"Error: {e}")
    except Exception as e:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name"])
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
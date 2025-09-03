import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access(root_dir):
    companies = set()
    ads_and_businesses_dir = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses")
    if os.path.exists(ads_and_businesses_dir):
        advertisers_file = os.path.join(ads_and_businesses_dir, "advertisers_using_your_activity_or_information.json")
        if os.path.exists(advertisers_file):
            with open(advertisers_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for advertiser in data.get("ig_custom_audiences_all_types", []):
                    companies.add(advertiser.get("advertiser_name", ""))
    return companies

def write_to_csv(companies):
    with open("query_responses/results.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name"])
        for company in companies:
            writer.writerow([company])

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")
        companies = get_companies_with_access(root_dir)
        write_to_csv(companies)
    except FileNotFoundError as e:
        raise FileNotFoundError("Error: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()
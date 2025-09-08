import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access_to_instagram_activity(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        advertisers_file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")

        if not os.path.exists(advertisers_file_path):
            return []

        with open(advertisers_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        advertisers = data.get("ig_custom_audiences_all_types", [])
        companies = [advertiser.get("advertiser_name", "") for advertiser in advertisers]

        return companies

    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: {e}")

def write_to_csv(companies):
    try:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Company Name"])
            for company in companies:
                writer.writerow([company])
    except Exception as e:
        raise Exception(f"Error: {e}")

def main():
    try:
        companies = get_companies_with_access_to_instagram_activity(root_dir)
        write_to_csv(companies)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
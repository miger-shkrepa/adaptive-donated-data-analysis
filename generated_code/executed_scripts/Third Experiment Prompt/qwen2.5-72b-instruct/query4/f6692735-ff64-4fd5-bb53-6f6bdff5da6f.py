import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access_to_instagram_activity(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        companies = set()

        ads_and_businesses_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses")
        if os.path.exists(ads_and_businesses_path):
            advertisers_file_path = os.path.join(ads_and_businesses_path, "advertisers_using_your_activity_or_information.json")
            if os.path.exists(advertisers_file_path):
                with open(advertisers_file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    for advertiser in data.get("ig_custom_audiences_all_types", []):
                        companies.add(advertiser.get("advertiser_name", ""))

        # Save the results to a CSV file with utf-8 encoding
        os.makedirs('query_responses', exist_ok=True)
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Company Name"])
            for company in companies:
                writer.writerow([company])

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

# Call the function with the root directory
get_companies_with_access_to_instagram_activity(root_dir)
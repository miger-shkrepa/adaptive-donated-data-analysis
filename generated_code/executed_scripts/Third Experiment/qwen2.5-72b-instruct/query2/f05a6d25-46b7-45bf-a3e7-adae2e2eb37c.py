import os
import json
import csv

root_dir = "root_dir"

def process_ads_data(root_dir):
    ads_data_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "ads_about_meta.json")
    advertisers_data_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")

    ads_data = []
    advertisers_data = []

    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        if os.path.exists(ads_data_path):
            with open(ads_data_path, 'r') as file:
                ads_data = json.load(file)
        else:
            print("Warning: ads_about_meta.json not found. Assuming no ads data.")

        if os.path.exists(advertisers_data_path):
            with open(advertisers_data_path, 'r') as file:
                advertisers_data = json.load(file)
        else:
            print("Warning: advertisers_using_your_activity_or_information.json not found. Assuming no advertisers data.")

    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")

    company_ads_count = {}

    for entry in ads_data.get("label_values", []):
        label = entry.get("label")
        value = entry.get("value")
        if label and value:
            company_ads_count[label] = company_ads_count.get(label, 0) + 1

    for entry in advertisers_data.get("ig_custom_audiences_all_types", []):
        advertiser_name = entry.get("advertiser_name")
        if advertiser_name:
            company_ads_count[advertiser_name] = company_ads_count.get(advertiser_name, 0) + 1

    return company_ads_count

def write_to_csv(data, output_path):
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Company Name', 'Number of Ads Viewed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for company, count in data.items():
            writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})

try:
    ads_data = process_ads_data(root_dir)
    write_to_csv(ads_data, 'query_responses/results.csv')
except Exception as e:
    print(f"An error occurred: {e}")
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Company Name', 'Number of Ads Viewed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
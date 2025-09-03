import os
import json
import csv

root_dir = "root_dir"

def get_advertisers_data(root_dir):
    advertisers_file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")
    
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.exists(advertisers_file_path):
        raise FileNotFoundError("FileNotFoundError: The advertisers file does not exist.")
    
    with open(advertisers_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    advertisers = data.get("ig_custom_audiences_all_types", [])
    return advertisers

def generate_csv(advertisers):
    output_path = 'query_responses/results.csv'
    
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name", "Number of Ads Viewed"])
        
        for advertiser in advertisers:
            company_name = advertiser.get("advertiser_name", "Unknown")
            writer.writerow([company_name, 0])

try:
    advertisers_data = get_advertisers_data(root_dir)
    generate_csv(advertisers_data)
except FileNotFoundError as e:
    print(e)
    generate_csv([])  # Generate an empty CSV with headers if the file is not found
except Exception as e:
    print(f"Error: An unexpected error occurred - {e}")
    generate_csv([])  # Generate an empty CSV with headers if an unexpected error occurs
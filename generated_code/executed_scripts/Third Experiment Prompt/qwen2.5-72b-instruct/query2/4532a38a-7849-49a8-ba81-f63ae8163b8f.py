import os
import json
import csv

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def process_ads_viewed(file_path):
    try:
        data = load_json(file_path)
        ads_viewed = data.get("impressions_history_ads_seen", [])
        return len(ads_viewed)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0

def process_advertisers(file_path):
    try:
        data = load_json(file_path)
        advertisers = data.get("ig_custom_audiences_all_types", [])
        return {advertiser.get("advertiser_name", "Unknown"): 0 for advertiser in advertisers}
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return {}

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    ads_viewed_count = 0
    advertisers = {}

    ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
    if os.path.exists(ads_viewed_path):
        ads_viewed_count = process_ads_viewed(ads_viewed_path)

    advertisers_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")
    if os.path.exists(advertisers_path):
        advertisers = process_advertisers(advertisers_path)

    # Update the number of ads viewed for each advertiser
    for advertiser in advertisers:
        advertisers[advertiser] = ads_viewed_count

    # Write the results to a CSV file
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Company Name', 'Number of Ads Viewed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for company, count in advertisers.items():
            writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
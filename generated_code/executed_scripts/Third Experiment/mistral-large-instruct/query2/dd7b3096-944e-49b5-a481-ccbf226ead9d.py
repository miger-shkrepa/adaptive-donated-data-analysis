import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Initialize a dictionary to store the results
results = {}

# Function to process the ads_viewed.json file
def process_ads_viewed(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for ad in data.get('impressions_history_ads_seen', []):
                time_data = ad.get('string_map_data', {}).get('Time', {})
                timestamp = time_data.get('timestamp', 0)
                if timestamp:
                    if 'Unknown Company' not in results:
                        results['Unknown Company'] = 0
                    results['Unknown Company'] += 1
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The ads_viewed.json file is not a valid JSON.")

# Function to process the advertisers_using_your_activity_or_information.json file
def process_advertisers_info(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for advertiser in data.get('ig_custom_audiences_all_types', []):
                company_name = advertiser.get('advertiser_name', 'Unknown Company')
                if company_name not in results:
                    results[company_name] = 0
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The advertisers_using_your_activity_or_information.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The advertisers_using_your_activity_or_information.json file is not a valid JSON.")

# Main function to process the directory
def main():
    ads_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')
    advertisers_info_path = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'advertisers_using_your_activity_or_information.json')

    try:
        process_advertisers_info(advertisers_info_path)
        process_ads_viewed(ads_viewed_path)

        # Write the results to the CSV file
        with open(output_csv, 'w', newline='') as csvfile:
            fieldnames = ['Company Name', 'Number of Ads Viewed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for company, count in results.items():
                writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})

    except Exception as e:
        print(e)
        # If an error occurs, create a CSV file with only the column headers
        with open(output_csv, 'w', newline='') as csvfile:
            fieldnames = ['Company Name', 'Number of Ads Viewed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

if __name__ == "__main__":
    main()
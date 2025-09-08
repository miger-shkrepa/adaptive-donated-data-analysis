import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to process the ads_viewed.json file
def process_ads_viewed(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            ads_seen = data.get('impressions_history_ads_seen', [])
            return ads_seen
    except FileNotFoundError:
        raise FileNotFoundError("Error: The ads_viewed.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The ads_viewed.json file is not a valid JSON.")

# Function to process the advertisers_using_your_activity_or_information.json file
def process_advertisers(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            advertisers = data.get('ig_custom_audiences_all_types', [])
            return advertisers
    except FileNotFoundError:
        raise FileNotFoundError("Error: The advertisers_using_your_activity_or_information.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The advertisers_using_your_activity_or_information.json file is not a valid JSON.")

# Main function to process the directory and generate the CSV
def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")

        ads_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')
        advertisers_path = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'advertisers_using_your_activity_or_information.json')

        ads_seen = process_ads_viewed(ads_viewed_path)
        advertisers = process_advertisers(advertisers_path)

        # Create a dictionary to count the number of ads viewed per company
        company_ads_count = {}
        for ad in ads_seen:
            author = ad.get('string_map_data', {}).get('Author', {}).get('value', '')
            if author:
                if author in company_ads_count:
                    company_ads_count[author] += 1
                else:
                    company_ads_count[author] = 1

        # Write the results to the CSV file
        with open(output_csv, 'w', newline='') as csvfile:
            fieldnames = ['Company Name', 'Number of Ads Viewed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for company, count in company_ads_count.items():
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
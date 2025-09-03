import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to extract ads viewed data
def extract_ads_viewed(root_dir):
    ads_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')
    if not os.path.exists(ads_viewed_path):
        raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")

    with open(ads_viewed_path, 'r') as file:
        data = json.load(file)

    ads_viewed_data = data.get('impressions_history_ads_seen', [])
    return ads_viewed_data

# Function to extract advertisers data
def extract_advertisers(root_dir):
    advertisers_path = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'advertisers_using_your_activity_or_information.json')
    if not os.path.exists(advertisers_path):
        raise FileNotFoundError("FileNotFoundError: The advertisers_using_your_activity_or_information.json file does not exist.")

    with open(advertisers_path, 'r') as file:
        data = json.load(file)

    advertisers_data = data.get('ig_custom_audiences_all_types', [])
    return advertisers_data

# Function to generate the CSV file
def generate_csv(ads_viewed_data, advertisers_data):
    if not os.path.exists('query_responses'):
        os.makedirs('query_responses')

    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Company Name', 'Number of Ads Viewed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        # Create a dictionary to count ads viewed by company
        ads_count = {}
        for ad in ads_viewed_data:
            author = ad.get('string_map_data', {}).get('Author', {}).get('value', 'Unknown')
            if author in ads_count:
                ads_count[author] += 1
            else:
                ads_count[author] = 1

        # Write the data to the CSV file
        for company in advertisers_data:
            company_name = company.get('advertiser_name', 'Unknown')
            number_of_ads = ads_count.get(company_name, 0)
            writer.writerow({'Company Name': company_name, 'Number of Ads Viewed': number_of_ads})

# Main function to execute the script
def main():
    try:
        ads_viewed_data = extract_ads_viewed(root_dir)
        advertisers_data = extract_advertisers(root_dir)
        generate_csv(ads_viewed_data, advertisers_data)
    except FileNotFoundError as e:
        print(e)
        # Create an empty CSV file with headers if required files are missing
        if not os.path.exists('query_responses'):
            os.makedirs('query_responses')
        with open(output_csv, 'w', newline='') as csvfile:
            fieldnames = ['Company Name', 'Number of Ads Viewed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
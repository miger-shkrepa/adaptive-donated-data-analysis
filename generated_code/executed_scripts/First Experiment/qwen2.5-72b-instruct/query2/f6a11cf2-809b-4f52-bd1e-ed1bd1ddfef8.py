import os
import json
import csv
from collections import defaultdict

# Define the root directory
root_dir = "root_dir"

# Function to read and parse JSON files
def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to process ads_viewed.json and extract company names and ad counts
def process_ads_viewed(data):
    ad_counts = defaultdict(int)
    for impression in data.get('impressions_history_ads_seen', []):
        string_map_data = impression.get('string_map_data', {})
        author = string_map_data.get('Author', {}).get('value')
        if author:
            ad_counts[author] += 1
    return ad_counts

# Function to process advertisers_using_your_activity_or_information.json and extract company names
def process_advertisers_using_activity(data):
    companies = set()
    for advertiser in data.get('ig_custom_audiences_all_types', []):
        company_name = advertiser.get('advertiser_name')
        if company_name:
            companies.add(company_name)
    return companies

# Main function to generate the CSV report
def generate_ad_report():
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    # Initialize a dictionary to store ad counts
    ad_counts = defaultdict(int)
    
    # Process ads_viewed.json
    ads_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')
    if os.path.exists(ads_viewed_path):
        ads_data = read_json(ads_viewed_path)
        ad_counts.update(process_ads_viewed(ads_data))
    
    # Process advertisers_using_your_activity_or_information.json
    advertisers_activity_path = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'advertisers_using_your_activity_or_information.json')
    if os.path.exists(advertisers_activity_path):
        advertisers_data = read_json(advertisers_activity_path)
        companies = process_advertisers_using_activity(advertisers_data)
        for company in companies:
            ad_counts[company] += 1
    
    # Write the results to a CSV file
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Company Name', 'Number of Ads Viewed'])
        for company, count in ad_counts.items():
            writer.writerow([company, count])

# Run the main function
if __name__ == "__main__":
    try:
        generate_ad_report()
        print("CSV report generated successfully.")
    except Exception as e:
        print(e)
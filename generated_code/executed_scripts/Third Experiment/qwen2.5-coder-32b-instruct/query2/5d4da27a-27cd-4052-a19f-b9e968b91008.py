import os
import json
import csv

# Variable referring to the file input
root_dir = "root_dir"

# Function to check if a file exists and raise an error if it does not
def check_file_exists(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")

# Function to read JSON file and return its content
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to extract company names and ad counts from ads_viewed.json
def extract_ads_viewed_data(ads_viewed_path):
    ads_viewed_data = read_json_file(ads_viewed_path)
    ad_counts = {}
    for entry in ads_viewed_data.get('impressions_history_ads_seen', []):
        author = entry['string_map_data']['Author']['value']
        ad_counts[author] = ad_counts.get(author, 0) + 1
    return ad_counts

# Function to extract company names from ads_about_meta.json
def extract_ads_about_meta_data(ads_about_meta_path):
    ads_about_meta_data = read_json_file(ads_about_meta_path)
    company_names = set()
    for label_value in ads_about_meta_data.get('label_values', []):
        if 'ent_field_name' in label_value and label_value['ent_field_name'] == 'Advertiser':
            company_names.add(label_value['value'])
    return company_names

# Main function to generate the CSV file
def generate_csv():
    ads_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')
    ads_about_meta_path = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'ads_about_meta.json')

    # Check if the necessary files exist
    if not os.path.exists(ads_viewed_path):
        print(f"Warning: The file {ads_viewed_path} does not exist. Ad counts will be based on available data.")
        ad_counts = {}
    else:
        ad_counts = extract_ads_viewed_data(ads_viewed_path)

    if not os.path.exists(ads_about_meta_path):
        print(f"Warning: The file {ads_about_meta_path} does not exist. Company names will be based on available data.")
        company_names = set()
    else:
        company_names = extract_ads_about_meta_data(ads_about_meta_path)

    # Combine data
    combined_data = {company: ad_counts.get(company, 0) for company in company_names}

    # Write to CSV
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Company Name', 'Number of Ads Viewed'])
        for company, count in combined_data.items():
            writer.writerow([company, count])

# Execute the main function
try:
    generate_csv()
except FileNotFoundError as e:
    print(e)
except ValueError as e:
    print(e)
import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Function to read JSON file
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to get ads viewed data
def get_ads_viewed_data(root_dir):
    ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
    if not os.path.exists(ads_viewed_path):
        return {}
    return read_json_file(ads_viewed_path)

# Function to get ads about meta data
def get_ads_about_meta_data(root_dir):
    ads_about_meta_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "ads_about_meta.json")
    if not os.path.exists(ads_about_meta_path):
        return {}
    return read_json_file(ads_about_meta_path)

# Function to aggregate ads data
def aggregate_ads_data(ads_viewed_data, ads_about_meta_data):
    ads_count_by_company = {}
    
    # Extract company names from ads_about_meta_data
    company_names = {}
    if 'label_values' in ads_about_meta_data:
        for label_value in ads_about_meta_data['label_values']:
            if label_value.get('ent_field_name') == 'advertiser_name':
                company_names[label_value['value']] = label_value['value']
    
    # Count ads viewed by company
    if 'impressions_history_ads_seen' in ads_viewed_data:
        for ad in ads_viewed_data['impressions_history_ads_seen']:
            author = ad['string_map_data'].get('Author', {}).get('value')
            if author in company_names:
                company_name = company_names[author]
                if company_name in ads_count_by_company:
                    ads_count_by_company[company_name] += 1
                else:
                    ads_count_by_company[company_name] = 1
    
    return ads_count_by_company

# Main function to process data and generate CSV
def main():
    try:
        # Get ads viewed data
        ads_viewed_data = get_ads_viewed_data(root_dir)
        
        # Get ads about meta data
        ads_about_meta_data = get_ads_about_meta_data(root_dir)
        
        # Aggregate ads data
        ads_count_by_company = aggregate_ads_data(ads_viewed_data, ads_about_meta_data)
        
        # Write to CSV
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name', 'Number of Ads Viewed'])
            for company, count in ads_count_by_company.items():
                writer.writerow([company, count])
    
    except Exception as e:
        # Write only headers if any error occurs
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name', 'Number of Ads Viewed'])

# Execute the main function
if __name__ == "__main__":
    main()
import os
import json
import csv

root_dir = "root_dir"

def get_instagram_ads_companies(root_dir):
    try:
        advertisers_file_path = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'advertisers_using_your_activity_or_information.json')
        
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        if not os.path.exists(advertisers_file_path):
            return []
        
        with open(advertisers_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        advertisers = []
        for entry in data.get('ig_custom_audiences_all_types', []):
            if entry.get('advertiser_name'):
                advertisers.append(entry['advertiser_name'])
        
        return advertisers
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

def write_to_csv(companies, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name'])
            for company in companies:
                writer.writerow([company])
    except Exception as e:
        raise Exception(f"Error: An error occurred while writing to CSV - {e}")

def main():
    try:
        companies = get_instagram_ads_companies(root_dir)
        output_path = 'query_responses/results.csv'
        write_to_csv(companies, output_path)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
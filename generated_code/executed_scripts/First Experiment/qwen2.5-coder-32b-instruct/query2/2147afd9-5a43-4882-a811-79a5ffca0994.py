import os
import csv
import json

root_dir = "root_dir"

def main():
    ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
    
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    # Check if the ads_viewed.json file exists
    if not os.path.exists(ads_viewed_path):
        raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")
    
    try:
        with open(ads_viewed_path, 'r', encoding='utf-8') as file:
            ads_data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError("ValueError: The ads_viewed.json file is not a valid JSON file.")
    
    # Dictionary to hold company names and their ad counts
    company_ads_count = {}
    
    # Extracting data from the JSON structure
    for impression in ads_data.get("impressions_history_ads_seen", []):
        author = impression.get("string_map_data", {}).get("Author", {}).get("value")
        if author:
            if author in company_ads_count:
                company_ads_count[author] += 1
            else:
                company_ads_count[author] = 1
    
    # Prepare the CSV file path
    csv_file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    
    # Writing to CSV
    try:
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            for company, count in company_ads_count.items():
                writer.writerow([company, count])
    except IOError:
        raise IOError("IOError: Failed to write to the CSV file.")

if __name__ == "__main__":
    main()
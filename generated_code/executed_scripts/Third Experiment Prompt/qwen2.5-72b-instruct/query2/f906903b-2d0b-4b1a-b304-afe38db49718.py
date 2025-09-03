import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Function to read JSON file and return its content
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

# Function to process ads_viewed.json and extract company names and ad counts
def process_ads_viewed(file_path):
    try:
        data = read_json_file(file_path)
        ads_data = data.get("impressions_history_ads_seen", [])
        
        ad_counts = {}
        for ad in ads_data:
            string_map_data = ad.get("string_map_data", {})
            author = string_map_data.get("Author", {}).get("value")
            if author:
                ad_counts[author] = ad_counts.get(author, 0) + 1
        
        return ad_counts
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return {}

# Function to generate the CSV file
def generate_csv(ad_counts):
    csv_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Company Name', 'Number of Ads Viewed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        if not ad_counts:
            return
        
        for company, count in ad_counts.items():
            writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})

# Main function to execute the query
def main():
    try:
        ads_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')
        
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        if not os.path.exists(ads_viewed_path):
            print("Warning: ads_viewed.json not found. Generating CSV with headers only.")
            generate_csv({})
            return
        
        ad_counts = process_ads_viewed(ads_viewed_path)
        generate_csv(ad_counts)
        
        print("CSV file generated successfully at query_responses/results.csv")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
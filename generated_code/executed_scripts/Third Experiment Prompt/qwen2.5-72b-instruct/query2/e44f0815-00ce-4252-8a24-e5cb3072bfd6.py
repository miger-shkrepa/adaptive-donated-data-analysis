import os
import json
import csv

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def process_ads_data(root_dir):
    ads_data = {}
    ads_file_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
    
    if not os.path.exists(ads_file_path):
        return ads_data

    try:
        ads_json = load_json_file(ads_file_path)
        impressions_history = ads_json.get('impressions_history_posts_seen', [])
        
        for impression in impressions_history:
            string_map_data = impression.get('string_map_data', {})
            author = string_map_data.get('Author', {}).get('value', '')
            if author:
                ads_data[author] = ads_data.get(author, 0) + 1
    except Exception as e:
        raise ValueError(f"Error: Failed to process ads data - {str(e)}")

    return ads_data

def write_to_csv(data, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Company Name', 'Number of Ads Viewed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            if not data:
                return
            
            for company, count in data.items():
                writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})
    except Exception as e:
        raise ValueError(f"Error: Failed to write to CSV - {str(e)}")

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    try:
        ads_data = process_ads_data(root_dir)
        output_path = 'query_responses/results.csv'
        write_to_csv(ads_data, output_path)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
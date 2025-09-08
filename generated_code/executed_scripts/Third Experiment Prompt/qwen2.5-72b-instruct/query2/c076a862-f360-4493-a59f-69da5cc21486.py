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

def count_ads_viewed(root_dir):
    ads_viewed = {}
    
    ads_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
    if os.path.exists(ads_path):
        try:
            ads_data = load_json_file(ads_path)
            for entry in ads_data.get('impressions_history_posts_seen', []):
                string_map_data = entry.get('string_map_data', {})
                author = string_map_data.get('Author', {}).get('value', 'Unknown')
                ads_viewed[author] = ads_viewed.get(author, 0) + 1
        except (FileNotFoundError, ValueError) as e:
            print(f"Error processing {ads_path}: {e}")
    
    return ads_viewed

def write_to_csv(data, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Company Name', 'Number of Ads Viewed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for company, count in data.items():
            writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    try:
        ads_viewed = count_ads_viewed(root_dir)
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        write_to_csv(ads_viewed, output_path)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
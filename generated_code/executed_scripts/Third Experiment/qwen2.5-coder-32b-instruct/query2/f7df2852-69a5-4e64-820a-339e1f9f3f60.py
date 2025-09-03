import os
import csv
import json

root_dir = "root_dir"

def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

def get_ads_viewed_data(root_directory):
    ads_viewed_data = []
    ads_viewed_file_path = os.path.join(root_directory, 'ads_information', 'ads_and_topics', 'ads_viewed.json')
    
    if not os.path.exists(ads_viewed_file_path):
        return ads_viewed_data
    
    ads_viewed_content = read_json_file(ads_viewed_file_path)
    
    if 'impressions_history_ads_seen' in ads_viewed_content:
        for entry in ads_viewed_content['impressions_history_ads_seen']:
            if 'string_map_data' in entry and 'Author' in entry['string_map_data']:
                ads_viewed_data.append(entry['string_map_data']['Author']['value'])
    
    return ads_viewed_data

def generate_csv(ads_viewed_data):
    try:
        os.makedirs('query_responses', exist_ok=True)
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Company Name', 'Number of Ads Viewed'])
            
            ads_count = {}
            for company in ads_viewed_data:
                if company in ads_count:
                    ads_count[company] += 1
                else:
                    ads_count[company] = 1
            
            for company, count in ads_count.items():
                csvwriter.writerow([company, count])
    except Exception as e:
        raise Exception(f"Error: Failed to write CSV file. {str(e)}")

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.isdir(root_dir):
        raise ValueError("ValueError: The root directory is not a valid directory.")
    
    ads_viewed_data = get_ads_viewed_data(root_dir)
    generate_csv(ads_viewed_data)

if __name__ == "__main__":
    main()
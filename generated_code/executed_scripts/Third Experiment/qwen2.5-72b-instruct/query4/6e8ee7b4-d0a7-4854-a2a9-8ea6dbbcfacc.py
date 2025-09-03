import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access(root_directory):
    companies = set()
    try:
        if not os.path.exists(root_directory):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        ads_info_path = os.path.join(root_directory, "ads_information")
        if not os.path.exists(ads_info_path):
            return companies  # Return empty set if the directory does not exist
        
        for file_name in ["ads_viewed.json", "posts_viewed.json", "videos_watched.json"]:
            file_path = os.path.join(ads_info_path, "ads_and_topics", file_name)
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    for entry in data.get("impressions_history_ads_seen", []):
                        author = entry.get("string_map_data", {}).get("Author", {}).get("value")
                        if author:
                            companies.add(author)
                    for entry in data.get("impressions_history_posts_seen", []):
                        author = entry.get("string_map_data", {}).get("Author", {}).get("value")
                        if author:
                            companies.add(author)
                    for entry in data.get("impressions_history_videos_watched", []):
                        author = entry.get("string_map_data", {}).get("Author", {}).get("value")
                        if author:
                            companies.add(author)
        
        return companies
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

def write_to_csv(companies, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Company Name"])
            for company in companies:
                writer.writerow([company])
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

try:
    companies_with_access = get_companies_with_access(root_dir)
    write_to_csv(companies_with_access, 'query_responses/results.csv')
except Exception as e:
    print(str(e))
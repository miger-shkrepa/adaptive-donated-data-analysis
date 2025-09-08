import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access_to_instagram_activity(root_directory):
    companies_with_access = set()
    
    try:
        if not os.path.exists(root_directory):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        instagram_activity_path = os.path.join(root_directory, "your_instagram_activity")
        
        if not os.path.exists(instagram_activity_path):
            return companies_with_access
        
        for root, dirs, files in os.walk(instagram_activity_path):
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if "media_metadata" in data and "video_metadata" in data["media_metadata"]:
                            for video in data["media_metadata"]["video_metadata"]["exif_data"]:
                                if "device_id" in video:
                                    companies_with_access.add(video["device_id"])
        
        return companies_with_access
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

def write_to_csv(companies, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Company Name"])
            for company in companies:
                writer.writerow([company])
    except Exception as e:
        raise Exception(f"Error: An error occurred while writing to CSV - {e}")

try:
    companies_with_access = get_companies_with_access_to_instagram_activity(root_dir)
    write_to_csv(companies_with_access, 'query_responses/results.csv')
except Exception as e:
    print(e)
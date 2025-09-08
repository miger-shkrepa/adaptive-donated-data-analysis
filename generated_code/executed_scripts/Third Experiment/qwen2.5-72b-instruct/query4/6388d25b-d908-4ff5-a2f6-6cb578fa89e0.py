import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access_to_instagram_activity(root_dir):
    companies_with_access = set()
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Check if the required directory exists
        instagram_activity_path = os.path.join(root_dir, "your_instagram_activity")
        if not os.path.exists(instagram_activity_path):
            return companies_with_access

        # Iterate through the files in the 'your_instagram_activity' directory
        for subdir, dirs, files in os.walk(instagram_activity_path):
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(subdir, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        try:
                            data = json.load(f)
                            if "cross_post_source" in str(data):
                                for item in data:
                                    if isinstance(data[item], list):
                                        for entry in data[item]:
                                            if "cross_post_source" in entry and "source_app" in entry["cross_post_source"]:
                                                companies_with_access.add(entry["cross_post_source"]["source_app"])
                        except json.JSONDecodeError:
                            raise ValueError("Error: Failed to decode JSON file.")

    except Exception as e:
        raise e

    return companies_with_access

def write_to_csv(companies_with_access):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name"])
        for company in companies_with_access:
            writer.writerow([company])

try:
    companies_with_access = get_companies_with_access_to_instagram_activity(root_dir)
    write_to_csv(companies_with_access)
except Exception as e:
    print(e)
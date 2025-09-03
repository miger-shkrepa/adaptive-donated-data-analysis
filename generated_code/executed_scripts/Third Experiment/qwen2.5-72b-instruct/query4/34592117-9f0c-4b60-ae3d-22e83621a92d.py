import os
import csv
import json

root_dir = "root_dir"

def get_companies_with_access_to_activity(root_dir):
    companies = set()
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        activity_path = os.path.join(root_dir, "activity")
        if not os.path.exists(activity_path):
            return companies

        for root, dirs, files in os.walk(activity_path):
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if "string_list_data" in data:
                            for item in data["string_list_data"]:
                                if "value" in item:
                                    companies.add(item["value"])
        
        return companies

    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

def save_to_csv(companies):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name"])
        for company in companies:
            writer.writerow([company])

try:
    companies_with_access = get_companies_with_access_to_activity(root_dir)
    save_to_csv(companies_with_access)
except Exception as e:
    print(e)
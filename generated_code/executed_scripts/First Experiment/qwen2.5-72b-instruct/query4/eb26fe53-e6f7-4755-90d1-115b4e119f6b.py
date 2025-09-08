import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access_to_instagram_activity(root_directory):
    companies_with_access = set()

    try:
        if not os.path.exists(root_directory):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        for dirpath, dirnames, filenames in os.walk(root_directory):
            for filename in filenames:
                if filename.endswith('.json'):
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        try:
                            data = json.load(file)
                            if 'your_instagram_activity' in dirpath:
                                for key, value in data.items():
                                    if isinstance(value, dict) and 'string_map_data' in value:
                                        for sub_key, sub_value in value['string_map_data'].items():
                                            if 'User Agent' in sub_key:
                                                user_agent = sub_value.get('value')
                                                if user_agent:
                                                    company = user_agent.split('/')[0]
                                                    companies_with_access.add(company)
                        except json.JSONDecodeError:
                            raise ValueError("Error: JSON decoding error in file " + file_path)

    except Exception as e:
        raise e

    return companies_with_access

def save_to_csv(companies, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name'])
            for company in companies:
                writer.writerow([company])
    except Exception as e:
        raise e

try:
    companies_with_access = get_companies_with_access_to_instagram_activity(root_dir)
    save_to_csv(companies_with_access, 'query_responses/results.csv')
except Exception as e:
    print(str(e))
import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access_to_instagram_activity(root_directory):
    try:
        if not os.path.exists(root_directory):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        companies_with_access = set()
        
        for dirpath, dirnames, filenames in os.walk(root_directory):
            for filename in filenames:
                if filename.endswith('.json'):
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
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
        
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name'])
            for company in companies_with_access:
                writer.writerow([company])
                
    except FileNotFoundError as e:
        print(e)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

# Call the function with the root directory
get_companies_with_access_to_instagram_activity(root_dir)
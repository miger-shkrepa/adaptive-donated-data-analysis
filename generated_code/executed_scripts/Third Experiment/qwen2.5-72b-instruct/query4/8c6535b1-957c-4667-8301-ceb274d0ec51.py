import os
import csv
import json

root_dir = "root_dir"

def get_companies_with_access(root):
    companies = set()
    try:
        if not os.path.exists(root):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        for dirpath, dirnames, filenames in os.walk(root):
            for filename in filenames:
                if filename.endswith('.json'):
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        if 'string_map_data' in data and 'User Agent' in data['string_map_data']:
                            user_agent = data['string_map_data']['User Agent']['value']
                            if 'company' in user_agent:
                                companies.add(user_agent.split('company=')[1].split(';')[0])
        
        if not companies:
            return []
        
        return list(companies)
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise ValueError(f"Error: An unexpected error occurred - {e}")

def write_to_csv(companies):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Company Name'])
        for company in companies:
            writer.writerow([company])

try:
    companies_with_access = get_companies_with_access(root_dir)
    write_to_csv(companies_with_access)
except Exception as e:
    print(e)
import os
import json
import csv

root_dir = "root_dir"

def extract_company_names_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            company_names = set()

            def traverse_json(obj):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        if key == 'value' and isinstance(value, str):
                            company_names.add(value)
                        else:
                            traverse_json(value)
                elif isinstance(obj, list):
                    for item in obj:
                        traverse_json(item)

            traverse_json(data)
            return company_names
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON file.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def find_company_access(root_dir):
    company_names = set()
    try:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith('.json'):
                    file_path = os.path.join(dirpath, filename)
                    try:
                        company_names.update(extract_company_names_from_json(file_path))
                    except FileNotFoundError:
                        print(f"Warning: JSON file {file_path} does not exist.")
                    except Exception as e:
                        print(f"Warning: Failed to process {file_path}. {str(e)}")
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")
    return company_names

def save_to_csv(company_names):
    try:
        os.makedirs('query_responses', exist_ok=True)
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name'])
            for company in company_names:
                writer.writerow([company])
    except Exception as e:
        raise Exception(f"Error: Failed to write to CSV file. {str(e)}")

if __name__ == "__main__":
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        company_names = find_company_access(root_dir)
        save_to_csv(company_names)
    except Exception as e:
        print(e)
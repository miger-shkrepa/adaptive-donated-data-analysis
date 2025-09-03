import os
import json
import csv

root_dir = "root_dir"

def get_company_names_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            company_names = set()
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict):
                                for sub_key, sub_value in item.items():
                                    if isinstance(sub_value, dict) and 'value' in sub_value:
                                        company_names.add(sub_value['value'])
            return company_names
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified file does not exist.")
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
                    company_names.update(get_company_names_from_json(file_path))
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")
    return company_names

def save_to_csv(company_names):
    try:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name'])
            for company in company_names:
                writer.writerow([company])
    except Exception as e:
        raise Exception(f"Error: Failed to write to CSV file. {str(e)}")

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        company_names = find_company_access(root_dir)
        save_to_csv(company_names)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
import os
import json
import csv

root_dir = "root_dir"

def get_company_names_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            company_names = set()

            def extract_company_names(obj):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        if isinstance(value, dict):
                            if 'value' in value:
                                company_names.add(value['value'])
                            else:
                                extract_company_names(value)
                        elif isinstance(value, list):
                            for item in value:
                                extract_company_names(item)
                elif isinstance(obj, list):
                    for item in obj:
                        extract_company_names(item)

            extract_company_names(data)
            return company_names
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON from the file.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred: {str(e)}")

def find_company_names_in_directory(directory):
    company_names = set()
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    try:
                        company_names.update(get_company_names_from_file(file_path))
                    except Exception as e:
                        print(f"Warning: Failed to process file {file_path}: {str(e)}")
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred: {str(e)}")
    return company_names

def save_to_csv(company_names, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name'])
            for company in company_names:
                writer.writerow([company])
    except Exception as e:
        raise Exception(f"Error: Failed to write to CSV file: {str(e)}")

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        company_names = find_company_names_in_directory(root_dir)
        
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        save_to_csv(company_names, output_path)
        
        print(f"CSV file saved to {output_path}")
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()
import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to extract company names from JSON files
def extract_company_names(directory):
    company_names = set()

    # Walk through the directory
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Extract company names from the JSON data
                        company_names.update(extract_from_json(data))
                except FileNotFoundError:
                    raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
                except json.JSONDecodeError:
                    raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

    return company_names

# Function to recursively extract company names from JSON data
def extract_from_json(data):
    company_names = set()
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "Company Name":
                company_names.add(value)
            elif isinstance(value, (dict, list)):
                company_names.update(extract_from_json(value))
    elif isinstance(data, list):
        for item in data:
            company_names.update(extract_from_json(item))
    return company_names

# Main function to execute the query
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    company_names = extract_company_names(root_dir)

    # Write the results to a CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name"])
        for name in company_names:
            writer.writerow([name])

if __name__ == "__main__":
    main()
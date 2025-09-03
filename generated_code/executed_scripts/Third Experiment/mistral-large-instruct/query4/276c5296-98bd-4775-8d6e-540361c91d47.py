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

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Extract company names from the JSON structure
                        company_names.update(extract_from_json(data))
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    raise FileNotFoundError(f"Error: {e}")

    return company_names

# Function to recursively extract company names from JSON structure
def extract_from_json(data):
    company_names = set()

    if isinstance(data, dict):
        for key, value in data.items():
            if key in ["company_name", "name", "value"] and isinstance(value, str):
                company_names.add(value)
            company_names.update(extract_from_json(value))
    elif isinstance(data, list):
        for item in data:
            company_names.update(extract_from_json(item))

    return company_names

# Main function to process the directory and generate the CSV file
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    company_names = extract_company_names(root_dir)

    # Write the results to a CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name"])
        for name in company_names:
            writer.writerow([name])

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
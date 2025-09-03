import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to extract company names from JSON files
def extract_company_names(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            company_names = []
            if 'label_values' in data:
                for item in data['label_values']:
                    if 'label' in item and 'value' in item:
                        company_names.append(item['value'])
            return company_names
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to process the directory and extract company names
def process_directory(root_dir):
    company_names = []
    try:
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file == "subscription_for_no_ads.json":
                    file_path = os.path.join(root, file)
                    company_names.extend(extract_company_names(file_path))
    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except ValueError as e:
        raise ValueError(f"ValueError: {e}")
    return company_names

# Function to write the results to a CSV file
def write_to_csv(company_names, output_csv):
    try:
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Company Name"])
            for name in company_names:
                writer.writerow([name])
    except Exception as e:
        raise Exception(f"Error: {e}")

# Main function to execute the script
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    company_names = process_directory(root_dir)

    if not company_names:
        company_names = [""]  # Add an empty row if no data is found

    write_to_csv(company_names, output_csv)

if __name__ == "__main__":
    main()
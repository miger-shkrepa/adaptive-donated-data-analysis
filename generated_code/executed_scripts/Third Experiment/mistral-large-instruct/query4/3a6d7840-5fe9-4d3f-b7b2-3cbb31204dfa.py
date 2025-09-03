import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Function to extract company names from JSON files
def extract_company_names(directory):
    company_names = set()

    # Walk through the directory structure
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        # Extract company names from the JSON data
                        company_names.update(extract_from_json(data))
                except FileNotFoundError:
                    raise FileNotFoundError("Error: The file does not exist.")
                except json.JSONDecodeError:
                    raise ValueError("Error: The file is not a valid JSON.")

    return company_names

# Function to extract company names from JSON data
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

# Main function to generate the CSV file
def generate_csv(directory):
    try:
        company_names = extract_company_names(directory)
        if not company_names:
            # If no company names are found, create a CSV with only the column header
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Company Name"])
        else:
            # Write the company names to the CSV file
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Company Name"])
                for name in company_names:
                    writer.writerow([name])
    except Exception as e:
        raise e

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("Error: The root directory does not exist.")

# Generate the CSV file
generate_csv(root_dir)
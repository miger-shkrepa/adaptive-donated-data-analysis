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

    # Walk through the directory structure
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Extract company names from the JSON data
                        company_names.update(extract_from_json(data))
                except FileNotFoundError:
                    raise FileNotFoundError(f"Error: FileNotFoundError: The file {file_path} does not exist.")
                except json.JSONDecodeError:
                    raise ValueError(f"Error: ValueError: The file {file_path} is not a valid JSON file.")

    return company_names

# Function to extract company names from JSON data
def extract_from_json(data):
    company_names = set()

    if isinstance(data, dict):
        for key, value in data.items():
            if key == "source_app":
                company_names.add(value)
            elif isinstance(value, (dict, list)):
                company_names.update(extract_from_json(value))
    elif isinstance(data, list):
        for item in data:
            company_names.update(extract_from_json(item))

    return company_names

# Main function to generate the CSV file
def generate_csv():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: FileNotFoundError: The root directory does not exist.")

    company_names = extract_company_names(root_dir)

    # Create the output directory if it does not exist
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    # Write the company names to the CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name"])
        for company in company_names:
            writer.writerow([company])

# Run the main function
if __name__ == "__main__":
    try:
        generate_csv()
        print(f"CSV file generated successfully at {output_csv}")
    except Exception as e:
        print(e)
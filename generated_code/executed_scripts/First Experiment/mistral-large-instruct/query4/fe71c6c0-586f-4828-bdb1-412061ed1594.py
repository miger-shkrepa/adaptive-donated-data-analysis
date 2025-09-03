import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Function to extract company names from JSON files
def extract_company_names(directory):
    company_names = set()

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Assuming company names are stored in specific fields
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
            if key in ["Company Name", "Media Owner"]:
                company_names.add(value)
            elif isinstance(value, (dict, list)):
                company_names.update(extract_from_json(value))
    elif isinstance(data, list):
        for item in data:
            company_names.update(extract_from_json(item))

    return company_names

# Main function to execute the script
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    company_names = extract_company_names(root_dir)

    # Save the results to a CSV file
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name"])
        for name in company_names:
            writer.writerow([name])

if __name__ == "__main__":
    main()
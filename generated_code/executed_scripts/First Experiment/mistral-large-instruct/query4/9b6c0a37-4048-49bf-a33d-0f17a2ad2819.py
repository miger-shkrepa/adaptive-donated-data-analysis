import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv_path = 'query_responses/results.csv'

# Function to extract company names from JSON files
def extract_company_names(directory):
    company_names = set()

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Assuming company names are stored in a specific key, e.g., "Company Name"
                        if isinstance(data, dict):
                            for key, value in data.items():
                                if isinstance(value, list):
                                    for item in value:
                                        if isinstance(item, dict) and 'Company Name' in item:
                                            company_names.add(item['Company Name'])
                except json.JSONDecodeError:
                    raise ValueError("Error: Invalid JSON format in file {}".format(file_path))
                except Exception as e:
                    raise ValueError("Error: {}".format(str(e)))

    return company_names

# Main function to execute the query
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    try:
        company_names = extract_company_names(root_dir)

        # Write the results to a CSV file
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Company Name"])
            for name in company_names:
                csv_writer.writerow([name])

        print("Results saved to {}".format(output_csv_path))

    except Exception as e:
        raise e

if __name__ == "__main__":
    main()
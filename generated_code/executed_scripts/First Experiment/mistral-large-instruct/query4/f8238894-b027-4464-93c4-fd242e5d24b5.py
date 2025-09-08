import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to extract company names from the directory structure
def extract_company_names(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a list to store company names
        company_names = []

        # Walk through the directory structure
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith('.json'):
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r') as file:
                        try:
                            data = json.load(file)
                            # Extract company names from the JSON data
                            # This is a placeholder for the actual extraction logic
                            # You need to implement the logic to extract company names from the JSON structure
                            # For example, if the company names are stored in a specific field:
                            # company_names.extend(data.get('company_names', []))
                        except json.JSONDecodeError:
                            raise ValueError("ValueError: Failed to decode JSON file.")

        # Write the company names to a CSV file
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Company Name"])
            for company in company_names:
                writer.writerow([company])

    except Exception as e:
        raise e

# Call the function to extract company names
extract_company_names(root_dir)
import os
import json
import csv

root_dir = "root_dir"

try:
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    # Initialize an empty set to store unique company names
    company_names = set()

    # Iterate over all files in the root directory
    for dir_path, dir_names, file_names in os.walk(root_dir):
        for file_name in file_names:
            # Check if the file is a JSON file
            if file_name.endswith(".json"):
                file_path = os.path.join(dir_path, file_name)
                try:
                    # Open and load the JSON file
                    with open(file_path, 'r') as file:
                        data = json.load(file)

                    # Check if the JSON file contains company information
                    if "string_map_data" in str(data):
                        # Extract company names from the JSON file
                        for key, value in data.items():
                            if isinstance(value, dict) and "string_map_data" in value:
                                for string_key, string_value in value["string_map_data"].items():
                                    if "href" in string_value and "Company" in string_key:
                                        company_name = string_value["value"]
                                        company_names.add(company_name)

                except json.JSONDecodeError:
                    raise ValueError("ValueError: Failed to parse JSON file.")

    # Create a list of company names
    company_name_list = list(company_names)

    # Write the company names to a CSV file
    with open('query_responses/results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Company Name"])  # header
        for company_name in company_name_list:
            writer.writerow([company_name])

except FileNotFoundError as e:
    print(e)
except ValueError as e:
    print(e)
except Exception as e:
    print(f"An error occurred: {e}")
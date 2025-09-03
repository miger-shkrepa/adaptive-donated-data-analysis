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
                        # Iterate over the data to find company names
                        if isinstance(data, dict):
                            for key, value in data.items():
                                if isinstance(value, list):
                                    for item in value:
                                        if "string_map_data" in item:
                                            for company, info in item["string_map_data"].items():
                                                if "href" in info and "Company" in company:
                                                    company_names.add(company)
                                                elif "value" in info and "Company" in company:
                                                    company_names.add(company)
                                        elif "media_map_data" in item:
                                            for company, info in item["media_map_data"].items():
                                                if "href" in info and "Company" in company:
                                                    company_names.add(company)
                                                elif "value" in info and "Company" in company:
                                                    company_names.add(company)
                                elif isinstance(value, dict):
                                    if "string_map_data" in value:
                                        for company, info in value["string_map_data"].items():
                                            if "href" in info and "Company" in company:
                                                company_names.add(company)
                                            elif "value" in info and "Company" in company:
                                                company_names.add(company)
                                    elif "media_map_data" in value:
                                        for company, info in value["media_map_data"].items():
                                            if "href" in info and "Company" in company:
                                                company_names.add(company)
                                            elif "value" in info and "Company" in company:
                                                company_names.add(company)
                except json.JSONDecodeError:
                    raise ValueError("ValueError: The JSON file is not valid.")

    # Create the output CSV file
    with open('query_responses/results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Company Name"])
        for company in company_names:
            writer.writerow([company])

except FileNotFoundError as e:
    print(e)
except ValueError as e:
    print(e)
except Exception as e:
    print("Error: An unexpected error occurred -", str(e))
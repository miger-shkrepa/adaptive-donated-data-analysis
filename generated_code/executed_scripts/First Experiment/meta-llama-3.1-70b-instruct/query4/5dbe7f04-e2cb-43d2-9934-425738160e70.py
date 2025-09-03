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
                    if "string_map_data" in str(data) or "media_map_data" in str(data):
                        # Extract company names from the JSON file
                        if isinstance(data, dict):
                            if "string_map_data" in data:
                                for value in data["string_map_data"].values():
                                    if "href" in value and "value" in value:
                                        company_names.add(value["value"])
                            elif "media_map_data" in data:
                                for value in data["media_map_data"].values():
                                    if "title" in value:
                                        company_names.add(value["title"])
                        elif isinstance(data, list):
                            for item in data:
                                if "string_map_data" in item:
                                    for value in item["string_map_data"].values():
                                        if "href" in value and "value" in value:
                                            company_names.add(value["value"])
                                elif "media_map_data" in item:
                                    for value in item["media_map_data"].values():
                                        if "title" in value:
                                            company_names.add(value["title"])

                except json.JSONDecodeError:
                    raise ValueError("ValueError: The JSON file is malformed.")

    # Write the company names to a CSV file
    with open('query_responses/results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Company Name"])
        for company_name in company_names:
            writer.writerow([company_name])

except FileNotFoundError as e:
    print(e)
except ValueError as e:
    print(e)
except Exception as e:
    print(f"Error: {str(e)}")
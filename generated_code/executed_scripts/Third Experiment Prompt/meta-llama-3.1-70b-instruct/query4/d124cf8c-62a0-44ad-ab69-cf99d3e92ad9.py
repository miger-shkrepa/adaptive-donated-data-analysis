import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access(root_dir):
    companies = set()
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")

        # Iterate through directories and files
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith(".json"):
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        # Check if file contains relevant data
                        if "media_map_data" in data or "string_map_data" in data:
                            # Extract company names from data
                            if "media_map_data" in data:
                                for media_data in data["media_map_data"]:
                                    if "company_name" in media_data:
                                        companies.add(media_data["company_name"])
                            if "string_map_data" in data:
                                for string_data in data["string_map_data"]:
                                    if "company_name" in string_data:
                                        companies.add(string_data["company_name"])

        # Write results to CSV file
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Company Name"])  # header
            for company in companies:
                writer.writerow([company])

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

get_companies_with_access(root_dir)
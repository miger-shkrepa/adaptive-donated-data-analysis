import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        companies_with_access = set()

        # Iterate over the subdirectories in the root directory
        for subdir in os.listdir(root_dir):
            subdir_path = os.path.join(root_dir, subdir)

            # Check if the subdirectory is a directory
            if os.path.isdir(subdir_path):
                # Iterate over the files in the subdirectory
                for filename in os.listdir(subdir_path):
                    file_path = os.path.join(subdir_path, filename)

                    # Check if the file is a JSON file
                    if filename.endswith(".json"):
                        try:
                            # Open and load the JSON file
                            with open(file_path, "r") as file:
                                data = json.load(file)

                            # Check if the JSON file contains company information
                            if "string_map_data" in data:
                                for key, value in data["string_map_data"].items():
                                    # Check if the value contains company information
                                    if "href" in value and "Company" in value["href"]:
                                        company_name = value["href"].split("/")[-1]
                                        companies_with_access.add(company_name)

                        except json.JSONDecodeError:
                            raise ValueError("ValueError: Failed to parse JSON file.")

        return companies_with_access

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def save_to_csv(companies_with_access):
    try:
        # Save the companies with access to a CSV file
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name"])
            for company in companies_with_access:
                writer.writerow([company])

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def main():
    try:
        companies_with_access = get_companies_with_access(root_dir)
        save_to_csv(companies_with_access)

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {str(e)}")
    except ValueError as e:
        raise ValueError(f"ValueError: {str(e)}")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
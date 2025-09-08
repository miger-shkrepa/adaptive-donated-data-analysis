import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a set to store unique company names
        companies = set()

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
                                    # Check if the value contains a company name
                                    if "href" in value and "Company" in value["href"]:
                                        company_name = value["href"].split("/")[-1]
                                        companies.add(company_name)

                        except json.JSONDecodeError:
                            raise ValueError("ValueError: Invalid JSON file.")

        return companies

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def save_to_csv(companies, output_path):
    try:
        # Create the output directory if it does not exist
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the companies to a CSV file
        with open(output_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name"])
            for company in companies:
                writer.writerow([company])

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def main():
    try:
        companies = get_companies_with_access(root_dir)
        output_path = "query_responses/results.csv"
        save_to_csv(companies, output_path)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
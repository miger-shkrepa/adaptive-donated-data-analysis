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

        # Iterate through the directory structure
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename == "advertisers_using_your_activity_or_information.json":
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, "r", encoding="utf-8") as file:
                        data = json.load(file)
                        # Check if the file contains the required structure
                        if "ig_custom_audiences_all_types" in data:
                            for audience in data["ig_custom_audiences_all_types"]:
                                companies.add(audience["advertiser_name"])

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")

    return companies

def write_to_csv(companies):
    with open("query_responses/results.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name"])  # header
        for company in companies:
            writer.writerow([company])

def main():
    companies = get_companies_with_access(root_dir)
    write_to_csv(companies)

if __name__ == "__main__":
    main()
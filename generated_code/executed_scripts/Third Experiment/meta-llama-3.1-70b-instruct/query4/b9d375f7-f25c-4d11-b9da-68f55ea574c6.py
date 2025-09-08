import os
import csv

root_dir = "root_dir"

def get_companies_with_access(root_dir):
    companies = set()
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Iterate over all files and directories in the root directory
        for dir_path, dir_names, file_names in os.walk(root_dir):
            for file_name in file_names:
                if file_name.endswith(".json"):
                    file_path = os.path.join(dir_path, file_name)
                    try:
                        # Open and read the JSON file
                        with open(file_path, 'r') as file:
                            # Since the actual JSON data is not provided, we assume that the company names are in the 'title' or 'value' fields
                            # This is a simplification and may not work for all cases
                            for line in file:
                                if '"title"' in line or '"value"' in line:
                                    # Extract the company name
                                    company_name = line.split(':')[1].strip().strip('"')
                                    companies.add(company_name)
                    except Exception as e:
                        raise ValueError("Error: Failed to parse JSON file: " + str(e))

    except Exception as e:
        raise ValueError("Error: " + str(e))

    return companies

def write_to_csv(companies):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name"])
            for company in companies:
                writer.writerow([company])
    except Exception as e:
        raise ValueError("Error: Failed to write to CSV file: " + str(e))

def main():
    try:
        companies = get_companies_with_access(root_dir)
        if companies:
            write_to_csv(companies)
        else:
            # If no companies are found, write a CSV file with only the column header
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Company Name"])
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()
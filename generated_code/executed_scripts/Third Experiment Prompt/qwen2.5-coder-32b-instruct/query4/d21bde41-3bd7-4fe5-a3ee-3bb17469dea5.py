import os
import csv

# Define the root directory
root_dir = "root_dir"

# Define the path to the output CSV file
output_csv_path = 'query_responses/results.csv'

# Function to find files containing company information
def find_company_files(root_dir):
    company_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if "apps_and_websites" in dirpath and filename.endswith(".json"):
                company_files.append(os.path.join(dirpath, filename))
    return company_files

# Function to extract company names from JSON files
def extract_company_names(company_files):
    company_names = set()
    for file_path in company_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = eval(file.read())
                if isinstance(data, dict):
                    for key, value in data.items():
                        if isinstance(value, dict) and "label_values" in value:
                            for label_value in value["label_values"]:
                                if "label" in label_value and "value" in label_value:
                                    company_names.add(label_value["value"])
        except FileNotFoundError:
            raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
        except Exception as e:
            raise ValueError(f"ValueError: An error occurred while processing the file {file_path}: {str(e)}")
    return company_names

# Main function to execute the query
def main():
    try:
        # Find files that might contain company information
        company_files = find_company_files(root_dir)
        
        # Extract company names from the found files
        company_names = extract_company_names(company_files)
        
        # Write the company names to a CSV file
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Company Name"])
            for company_name in company_names:
                writer.writerow([company_name])
    
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Company Name"])
    except Exception as e:
        print(f"Error: {str(e)}")
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Company Name"])

# Execute the main function
if __name__ == "__main__":
    main()
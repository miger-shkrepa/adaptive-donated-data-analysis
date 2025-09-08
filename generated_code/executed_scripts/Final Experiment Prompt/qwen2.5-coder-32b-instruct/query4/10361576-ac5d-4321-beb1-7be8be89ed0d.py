import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the path to the JSON file
json_file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")

# Define the path to the output CSV file
output_csv_path = "query_responses/results.csv"

# Function to read JSON data from a file
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to write CSV data to a file
def write_csv_file(file_path, data):
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name"])
            writer.writerows(data)
    except IOError:
        raise IOError(f"IOError: Failed to write to the file {file_path}.")

# Main function to process the data and generate the CSV
def main():
    try:
        # Read the JSON data
        data = read_json_file(json_file_path)
        
        # Extract the company names
        company_names = []
        if "ig_custom_audiences_all_types" in data:
            for entry in data["ig_custom_audiences_all_types"]:
                if "advertiser_name" in entry:
                    company_names.append([entry["advertiser_name"]])
        
        # Write the company names to the CSV file
        write_csv_file(output_csv_path, company_names)
    
    except (FileNotFoundError, ValueError, IOError) as e:
        # If any error occurs, write only the column headers to the CSV file
        write_csv_file(output_csv_path, [])

# Execute the main function
if __name__ == "__main__":
    main()
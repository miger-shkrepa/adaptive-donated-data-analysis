import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the path to the JSON file
json_file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")

# Define the path to the output CSV file
output_csv_path = "query_responses/results.csv"

# Function to extract company names from the JSON file
def extract_company_names(json_file_path):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Check if the JSON file exists
        if not os.path.exists(json_file_path):
            raise FileNotFoundError("FileNotFoundError: The JSON file does not exist.")

        # Read the JSON file
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Extract company names
        company_names = []
        for entry in data.get("ig_custom_audiences_all_types", []):
            advertiser_name = entry.get("advertiser_name")
            if advertiser_name:
                company_names.append(advertiser_name)

        return company_names

    except FileNotFoundError as fnf_error:
        print(fnf_error)
        return []
    except ValueError as val_error:
        print(f"ValueError: {val_error}")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

# Function to write company names to a CSV file
def write_to_csv(company_names, output_csv_path):
    try:
        # Create the output directory if it does not exist
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

        # Write the company names to the CSV file
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Company Name"])
            for name in company_names:
                csvwriter.writerow([name])

    except Exception as e:
        print(f"Error: {e}")

# Main function to execute the script
def main():
    company_names = extract_company_names(json_file_path)
    write_to_csv(company_names, output_csv_path)

# Execute the main function
if __name__ == "__main__":
    main()
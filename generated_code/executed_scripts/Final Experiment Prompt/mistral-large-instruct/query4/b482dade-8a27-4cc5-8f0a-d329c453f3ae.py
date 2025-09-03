import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the path to the JSON file
json_file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")

# Define the path to the output CSV file
output_csv_path = "query_responses/results.csv"

# Function to extract company names
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
    except json.JSONDecodeError:
        raise ValueError("ValueError: Error decoding JSON from the file.")
    except Exception as e:
        raise ValueError(f"ValueError: An unexpected error occurred: {e}")

# Function to write company names to CSV
def write_to_csv(company_names, output_csv_path):
    try:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

        # Write to CSV
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Company Name"])
            for name in company_names:
                csvwriter.writerow([name])

    except Exception as e:
        raise ValueError(f"ValueError: An error occurred while writing to CSV: {e}")

# Main execution
if __name__ == "__main__":
    company_names = extract_company_names(json_file_path)
    write_to_csv(company_names, output_csv_path)
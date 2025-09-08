import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

def get_companies_with_access(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Define the path to the JSON file
        json_file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")

        # Check if the JSON file exists
        if not os.path.exists(json_file_path):
            print("Warning: The required JSON file does not exist. Returning an empty CSV file.")
            return []

        # Read the JSON file with utf-8 encoding
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Extract the list of companies
        companies = []
        for entry in data.get("ig_custom_audiences_all_types", []):
            companies.append(entry.get("advertiser_name", ""))

        return companies

    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

def write_to_csv(companies):
    # Define the output CSV file path
    output_file_path = 'query_responses/results.csv'

    # Create the directory if it does not exist
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # Write the companies to the CSV file with utf-8 encoding
    with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name"])  # Write the header
        for company in companies:
            writer.writerow([company])

# Get the list of companies with access
companies_with_access = get_companies_with_access(root_dir)

# Write the companies to the CSV file
write_to_csv(companies_with_access)
import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

def extract_company_names(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Define the path to the specific JSON file
        file_path = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'advertisers_using_your_activity_or_information.json')

        # Check if the specific JSON file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError("FileNotFoundError: The required JSON file does not exist.")

        # Read the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Extract company names
        company_names = [entry['advertiser_name'] for entry in data.get('ig_custom_audiences_all_types', [])]

        # Write the company names to a CSV file
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name'])
            for name in company_names:
                writer.writerow([name])

    except FileNotFoundError as fnf_error:
        # Handle file not found error
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name'])
        raise fnf_error

    except ValueError as ve_error:
        # Handle value error
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name'])
        raise ValueError("ValueError: Error processing the JSON file.")

    except Exception as e:
        # Handle any other exceptions
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name'])
        raise Exception(f"Error: {str(e)}")

# Execute the function
extract_company_names(root_dir)
import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Define the path to the JSON file
json_file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")

# Define the path to the output CSV file
csv_file_path = "query_responses/results.csv"

# Create the directory for the output file if it doesn't exist
os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

# Initialize a list to store the company names
company_names = []

try:
    # Check if the JSON file exists
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"FileNotFoundError: The file {json_file_path} does not exist.")
    
    # Open and read the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Extract the company names from the JSON data
    if "ig_custom_audiences_all_types" in data:
        for advertiser in data["ig_custom_audiences_all_types"]:
            if "advertiser_name" in advertiser:
                company_names.append(advertiser["advertiser_name"])
    else:
        raise ValueError("ValueError: The expected structure in the JSON file is missing.")
    
    # Write the company names to the CSV file
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name"])
        for name in company_names:
            writer.writerow([name])

except FileNotFoundError as fnf_error:
    # If the file is not found, create an empty CSV with only the header
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name"])
    print(fnf_error)

except ValueError as ve_error:
    # If the JSON structure is incorrect, create an empty CSV with only the header
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name"])
    print(ve_error)

except Exception as e:
    # Handle any other exceptions
    print(f"Error: An unexpected error occurred - {e}")
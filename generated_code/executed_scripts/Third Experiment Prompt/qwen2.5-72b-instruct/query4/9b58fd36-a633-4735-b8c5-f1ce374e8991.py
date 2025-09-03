import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Function to read and parse JSON files
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON file.")

# Function to get the list of companies with access to Instagram activity or information
def get_companies_with_access(root_dir):
    companies = set()
    
    # Construct the path to the JSON file
    json_file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")
    
    if not os.path.exists(json_file_path):
        return companies  # Return an empty set if the file does not exist
    
    try:
        data = read_json_file(json_file_path)
        advertisers = data.get("ig_custom_audiences_all_types", [])
        
        for advertiser in advertisers:
            companies.add(advertiser.get("advertiser_name", ""))
    
    except Exception as e:
        print(f"Error processing JSON file: {e}")
    
    return companies

# Main function to generate the CSV file
def generate_csv(companies, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Company Name"])  # Write the header
            
            for company in companies:
                writer.writerow([company])
    except Exception as e:
        raise Exception(f"Error: Failed to write CSV file. Reason: {e}")

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Get the list of companies with access
companies_with_access = get_companies_with_access(root_dir)

# Generate the CSV file
output_path = 'query_responses/results.csv'
generate_csv(companies_with_access, output_path)

print(f"CSV file generated at {output_path}")
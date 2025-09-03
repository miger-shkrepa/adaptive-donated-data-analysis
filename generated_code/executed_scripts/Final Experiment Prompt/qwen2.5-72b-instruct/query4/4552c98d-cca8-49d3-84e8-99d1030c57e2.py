import os
import json
import csv

root_dir = "root_dir"

def extract_company_names(root_dir):
    try:
        # Define the path to the JSON file
        json_file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")
        
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Check if the JSON file exists
        if not os.path.exists(json_file_path):
            # If the file does not exist, create a CSV with only the header
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Company Name'])
            return
        
        # Read the JSON file
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        
        # Extract the company names
        company_names = []
        for entry in data.get("ig_custom_audiences_all_types", []):
            company_name = entry.get("advertiser_name")
            if company_name:
                company_names.append(company_name)
        
        # Write the company names to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name'])
            for name in company_names:
                writer.writerow([name])
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

# Call the function with the root directory
extract_company_names(root_dir)
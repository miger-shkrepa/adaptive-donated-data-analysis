import os
import csv
import json

root_dir = "root_dir"

def find_companies_with_access(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Define the path to the JSON file containing advertisers information
        advertisers_file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")
        
        # Check if the advertisers file exists
        if not os.path.exists(advertisers_file_path):
            raise FileNotFoundError("FileNotFoundError: The advertisers file does not exist.")
        
        # Read the JSON file
        with open(advertisers_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Extract the list of advertisers
        advertisers = data.get("ig_custom_audiences_all_types", [])
        
        # Extract the names of the companies
        company_names = [advertiser.get("advertiser_name", "") for advertiser in advertisers]
        
        # Write the company names to a CSV file
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Company Name"])
            for name in company_names:
                writer.writerow([name])
    
    except FileNotFoundError as e:
        # Create an empty CSV file with only the column headers if the file is not found
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Company Name"])
        print(e)
    except json.JSONDecodeError:
        raise ValueError("ValueError: The file is not a valid JSON.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {str(e)}")

# Call the function to execute the script
find_companies_with_access(root_dir)
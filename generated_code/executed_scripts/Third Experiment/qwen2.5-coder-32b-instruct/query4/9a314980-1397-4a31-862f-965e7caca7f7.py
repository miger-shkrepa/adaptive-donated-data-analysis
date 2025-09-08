import os
import csv

root_dir = "root_dir"

def find_companies_with_access(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Define the path to the file containing advertisers information
        advertisers_file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")
        
        # Check if the advertisers file exists
        if not os.path.exists(advertisers_file_path):
            raise FileNotFoundError("FileNotFoundError: The advertisers file does not exist.")
        
        # Read the advertisers file
        with open(advertisers_file_path, 'r', encoding='utf-8') as file:
            import json
            data = json.load(file)
        
        # Extract company names
        company_names = []
        if 'ig_custom_audiences_all_types' in data:
            for entry in data['ig_custom_audiences_all_types']:
                if 'advertiser_name' in entry:
                    company_names.append(entry['advertiser_name'])
        
        # Write the company names to a CSV file
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name'])
            for name in company_names:
                writer.writerow([name])
    
    except FileNotFoundError as e:
        # Create a CSV file with only the column headers if the file is not found
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name'])
        print(e)
    except Exception as e:
        print(f"Error: An unexpected error occurred - {str(e)}")

# Call the function to execute the script
find_companies_with_access(root_dir)
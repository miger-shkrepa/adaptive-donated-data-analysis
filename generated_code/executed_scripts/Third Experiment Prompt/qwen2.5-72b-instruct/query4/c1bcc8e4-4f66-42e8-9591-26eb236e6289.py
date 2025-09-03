import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

def get_companies_with_access(root_dir):
    try:
        # Define the path to the JSON file
        json_file_path = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'advertisers_using_your_activity_or_information.json')
        
        # Check if the JSON file exists
        if not os.path.exists(json_file_path):
            return []
        
        # Read the JSON file
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Extract the companies with access
        companies = []
        for entry in data.get('ig_custom_audiences_all_types', []):
            companies.append(entry.get('advertiser_name', ''))
        
        return companies
    
    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The JSON file is not properly formatted.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def write_to_csv(companies):
    # Define the path to the output CSV file
    csv_file_path = 'query_responses/results.csv'
    
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    
    # Write the companies to the CSV file
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Company Name'])  # Write the header
        for company in companies:
            writer.writerow([company])

def main():
    try:
        companies = get_companies_with_access(root_dir)
        write_to_csv(companies)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
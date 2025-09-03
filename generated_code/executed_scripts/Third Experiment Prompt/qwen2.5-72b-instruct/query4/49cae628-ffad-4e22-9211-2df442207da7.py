import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

def get_companies_with_access(root_dir):
    try:
        # Define the path to the JSON file
        json_file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")
        
        # Check if the file exists
        if not os.path.exists(json_file_path):
            return []  # Return an empty list if the file does not exist
        
        # Read the JSON file
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Extract the list of companies
        companies = []
        if "ig_custom_audiences_all_types" in data:
            for entry in data["ig_custom_audiences_all_types"]:
                if "advertiser_name" in entry:
                    companies.append(entry["advertiser_name"])
        
        return companies
    
    except FileNotFoundError as e:
        print(e)
        return []
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

def write_to_csv(companies):
    try:
        # Define the path to the output CSV file
        csv_file_path = 'query_responses/results.csv'
        
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
        
        # Write the companies to the CSV file with utf-8 encoding
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Company Name"])  # Write the header
            for company in companies:
                writer.writerow([company])
    
    except Exception as e:
        raise Exception(f"Error: An error occurred while writing to CSV - {e}")

def main():
    try:
        companies = get_companies_with_access(root_dir)
        write_to_csv(companies)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
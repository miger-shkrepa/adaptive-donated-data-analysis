import os
import csv

# Variable referring to the file input
root_dir = "root_dir"

def find_advertisers(root_dir):
    # Define the path to the JSON file
    json_file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")
    
    # Check if the file exists
    if not os.path.exists(json_file_path):
        raise FileNotFoundError("FileNotFoundError: The file 'advertisers_using_your_activity_or_information.json' does not exist.")
    
    # Initialize a list to store company names
    company_names = []
    
    # Read the JSON file
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            import json
            data = json.load(file)
            
            # Extract advertiser names
            if "ig_custom_audiences_all_types" in data:
                for advertiser in data["ig_custom_audiences_all_types"]:
                    if "advertiser_name" in advertiser:
                        company_names.append(advertiser["advertiser_name"])
    except json.JSONDecodeError:
        raise ValueError("ValueError: The file 'advertisers_using_your_activity_or_information.json' is not a valid JSON file.")
    
    return company_names

def save_to_csv(company_names):
    # Define the path to the output CSV file
    csv_file_path = 'query_responses/results.csv'
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    
    # Write to the CSV file
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name"])
        for company in company_names:
            writer.writerow([company])

def main():
    try:
        company_names = find_advertisers(root_dir)
        save_to_csv(company_names)
    except FileNotFoundError as e:
        save_to_csv([])  # Save only the column headers if the file is not found
        print(e)
    except ValueError as e:
        save_to_csv([])  # Save only the column headers if there is a JSON decoding error
        print(e)

if __name__ == "__main__":
    main()
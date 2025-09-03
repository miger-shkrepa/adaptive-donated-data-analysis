import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access_to_activity(root_directory):
    try:
        advertisers_file_path = os.path.join(root_directory, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")
        
        if not os.path.exists(root_directory):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        if not os.path.exists(advertisers_file_path):
            # If the file is missing, return a CSV with only the header
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Company Name"])
            return
        
        with open(advertisers_file_path, 'r') as file:
            data = json.load(file)
        
        advertisers = data.get("advertisers_using_your_activity_or_information", {}).get("ig_custom_audiences_all_types", [])
        
        companies = []
        for advertiser in advertisers:
            companies.append(advertiser.get("advertiser_name", ""))
        
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Company Name"])
            for company in companies:
                writer.writerow([company])
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

# Call the function with the root directory
get_companies_with_access_to_activity(root_dir)
import os
import json
import csv

root_dir = "root_dir"

def process_ads_data(root_directory):
    ads_data = {}
    try:
        if not os.path.exists(root_directory):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        ads_path = os.path.join(root_directory, "ads")
        if not os.path.exists(ads_path):
            return ads_data  # Return empty data if ads directory does not exist
        
        for filename in os.listdir(ads_path):
            if filename.endswith(".json"):
                file_path = os.path.join(ads_path, filename)
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    for entry in data.get("ads_seen", []):
                        company_name = entry.get("company_name", "Unknown")
                        ads_data[company_name] = ads_data.get(company_name, 0) + 1
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")
    
    return ads_data

def write_to_csv(data, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
            fieldnames = ['Company Name', 'Number of Ads Viewed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for company, count in data.items():
                writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})
    except Exception as e:
        raise Exception(f"Error: An error occurred while writing to CSV - {e}")

try:
    ads_data = process_ads_data(root_dir)
    write_to_csv(ads_data, 'query_responses/results.csv')
except Exception as e:
    print(e)
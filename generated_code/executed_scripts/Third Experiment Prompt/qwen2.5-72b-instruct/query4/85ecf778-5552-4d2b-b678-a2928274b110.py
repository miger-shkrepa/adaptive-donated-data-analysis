import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

def get_instagram_advertisers(root_dir):
    try:
        # Define the path to the JSON file
        json_path = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'advertisers_using_your_activity_or_information.json')
        
        # Check if the JSON file exists
        if not os.path.exists(json_path):
            print("Warning: The required JSON file does not exist. Returning an empty CSV.")
            return []
        
        # Read the JSON file
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Extract the advertiser names
        advertisers = []
        for entry in data.get('ig_custom_audiences_all_types', []):
            advertiser_name = entry.get('advertiser_name')
            if advertiser_name:
                advertisers.append(advertiser_name)
        
        return advertisers
    
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

def write_to_csv(advertisers):
    # Define the output CSV file path
    csv_path = 'query_responses/results.csv'
    
    # Create the directory if it does not exist
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
    # Write the data to the CSV file
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Company Name'])  # Write the header
        for advertiser in advertisers:
            writer.writerow([advertiser])

def main():
    try:
        advertisers = get_instagram_advertisers(root_dir)
        write_to_csv(advertisers)
        print(f"CSV file has been created at {csv_path}")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Function to read JSON file
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to get the number of ads viewed
def get_ads_viewed_count(root_dir):
    ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
    if not os.path.exists(ads_viewed_path):
        return 0
    
    ads_viewed_data = read_json_file(ads_viewed_path)
    return len(ads_viewed_data.get("impressions_history_ads_seen", []))

# Function to get the list of advertisers
def get_advertisers(root_dir):
    advertisers_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")
    if not os.path.exists(advertisers_path):
        return []
    
    advertisers_data = read_json_file(advertisers_path)
    return advertisers_data.get("ig_custom_audiences_all_types", [])

# Main function to generate the CSV file
def generate_csv(root_dir):
    try:
        ads_viewed_count = get_ads_viewed_count(root_dir)
        advertisers = get_advertisers(root_dir)
        
        # Prepare the data for CSV
        data = []
        for advertiser in advertisers:
            data.append([advertiser.get("advertiser_name", "Unknown"), ads_viewed_count])
        
        # Write the CSV file
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Company Name", "Number of Ads Viewed"])
            csvwriter.writerows(data)
    
    except Exception as e:
        # If any error occurs, write only the headers
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Company Name", "Number of Ads Viewed"])
        print(f"Error: {e}")

# Ensure the output directory exists
os.makedirs('query_responses', exist_ok=True)

# Generate the CSV file
generate_csv(root_dir)
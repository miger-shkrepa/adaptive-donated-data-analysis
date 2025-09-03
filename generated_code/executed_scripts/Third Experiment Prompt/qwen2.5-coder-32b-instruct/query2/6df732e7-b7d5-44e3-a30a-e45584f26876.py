import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Define the path to the JSON file
ads_file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")

# Initialize a dictionary to store the company names and the number of ads viewed
ads_data = {}

# Function to process the JSON file and extract the required information
def process_ads_file(file_path):
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
        
        # Open and read the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Check if the expected structure is present
        if 'ig_custom_audiences_all_types' not in data:
            raise ValueError(f"ValueError: The file {file_path} does not contain the expected structure.")
        
        # Extract the company names and the number of ads viewed
        for advertiser in data['ig_custom_audiences_all_types']:
            company_name = advertiser.get('advertiser_name', 'Unknown Company')
            if company_name not in ads_data:
                ads_data[company_name] = 0
            
            # Increment the count based on the presence of custom audience types
            if advertiser.get('has_data_file_custom_audience', False):
                ads_data[company_name] += 1
            if advertiser.get('has_in_person_store_visit', False):
                ads_data[company_name] += 1
            if advertiser.get('has_remarketing_custom_audience', False):
                ads_data[company_name] += 1
    
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except ValueError as ve_error:
        print(ve_error)
    except Exception as e:
        print(f"Error: An unexpected error occurred while processing the file {file_path}: {e}")

# Process the ads file
process_ads_file(ads_file_path)

# Define the path to the output CSV file
output_csv_path = 'query_responses/results.csv'

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

# Write the results to the CSV file
with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Company Name', 'Number of Ads Viewed'])
    for company, count in ads_data.items():
        csvwriter.writerow([company, count])

print(f"Results have been saved to {output_csv_path}")
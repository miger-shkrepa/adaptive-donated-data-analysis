import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to process the ads_viewed.json file
def process_ads_viewed(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            ads_seen = data.get('impressions_history_ads_seen', [])
            return ads_seen
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file 'ads_viewed.json' does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file 'ads_viewed.json' is not a valid JSON file.")

# Function to process the advertisers_using_your_activity_or_information.json file
def process_advertisers(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            advertisers = data.get('ig_custom_audiences_all_types', [])
            return advertisers
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file 'advertisers_using_your_activity_or_information.json' does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file 'advertisers_using_your_activity_or_information.json' is not a valid JSON file.")

# Main function to process the directory and generate the CSV
def main():
    ads_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')
    advertisers_path = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'advertisers_using_your_activity_or_information.json')

    try:
        ads_seen = process_ads_viewed(ads_viewed_path)
        advertisers = process_advertisers(advertisers_path)
    except Exception as e:
        # If any error occurs, create a CSV with only the column headers
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
        print(e)
        return

    # Create a dictionary to count the number of ads viewed per company
    company_ads_count = {}
    for ad in ads_seen:
        author = ad.get('string_map_data', {}).get('Author', {}).get('value', 'Unknown')
        if author in company_ads_count:
            company_ads_count[author] += 1
        else:
            company_ads_count[author] = 1

    # Write the results to the CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name", "Number of Ads Viewed"])
        for company, count in company_ads_count.items():
            writer.writerow([company, count])

if __name__ == "__main__":
    main()
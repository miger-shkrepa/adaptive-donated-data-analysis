import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to read JSON files
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: ValueError: The file {file_path} is not a valid JSON file.")

# Function to process ads viewed data
def process_ads_viewed(ads_viewed_path):
    ads_viewed_data = read_json_file(ads_viewed_path)
    ads_viewed_count = {}

    for ad in ads_viewed_data.get('impressions_history_ads_seen', []):
        author = ad.get('string_map_data', {}).get('Author', {}).get('value', 'Unknown')
        if author in ads_viewed_count:
            ads_viewed_count[author] += 1
        else:
            ads_viewed_count[author] = 1

    return ads_viewed_count

# Main function to process the directory and generate the CSV
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: FileNotFoundError: The root directory does not exist.")

    ads_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')

    if not os.path.exists(ads_viewed_path):
        # If the ads_viewed.json file does not exist, create a CSV with only the column headers
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Company Name', 'Number of Ads Viewed'])
        return

    ads_viewed_count = process_ads_viewed(ads_viewed_path)

    # Write the results to the CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Company Name', 'Number of Ads Viewed'])
        for company, count in ads_viewed_count.items():
            csv_writer.writerow([company, count])

if __name__ == "__main__":
    main()
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
            company_ads_count = {}
            for ad in ads_seen:
                author = ad.get('string_map_data', {}).get('Author', {}).get('value', 'Unknown')
                if author not in company_ads_count:
                    company_ads_count[author] = 0
                company_ads_count[author] += 1
            return company_ads_count
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The ads_viewed.json file is not a valid JSON.")

# Function to write the results to a CSV file
def write_to_csv(data):
    try:
        with open(output_csv, 'w', newline='') as csvfile:
            fieldnames = ['Company Name', 'Number of Ads Viewed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for company, count in data.items():
                writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})
    except Exception as e:
        raise ValueError(f"ValueError: Failed to write to CSV file. {str(e)}")

# Main function to process the directory and generate the CSV
def main():
    ads_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')

    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    if not os.path.exists(ads_viewed_path):
        # If the ads_viewed.json file does not exist, create a CSV with only the column headers
        write_to_csv({})
        return

    company_ads_count = process_ads_viewed(ads_viewed_path)
    write_to_csv(company_ads_count)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {str(e)}")
import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Function to process the ads_viewed.json file
def process_ads_viewed(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            ads_seen = data.get('impressions_history_ads_seen', [])
            return ads_seen
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The ads_viewed.json file is not a valid JSON.")

# Function to count ads by company
def count_ads_by_company(ads_seen):
    company_ads_count = {}
    for ad in ads_seen:
        author = ad.get('string_map_data', {}).get('Author', {}).get('value', 'Unknown')
        if author in company_ads_count:
            company_ads_count[author] += 1
        else:
            company_ads_count[author] = 1
    return company_ads_count

# Main function to process the directory and generate the CSV
def main():
    ads_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')

    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    ads_seen = process_ads_viewed(ads_viewed_path)
    company_ads_count = count_ads_by_company(ads_seen)

    # Write the results to a CSV file
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Company Name', 'Number of Ads Viewed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for company, count in company_ads_count.items():
            writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})

if __name__ == "__main__":
    main()
import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to extract ads viewed data
def extract_ads_viewed(root_dir):
    ads_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')
    if not os.path.exists(ads_viewed_path):
        raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")

    with open(ads_viewed_path, 'r') as file:
        data = json.load(file)

    ads_viewed_data = []
    for ad in data.get('impressions_history_ads_seen', []):
        author = ad.get('string_map_data', {}).get('Author', {}).get('value', 'Unknown')
        time = ad.get('string_map_data', {}).get('Time', {}).get('timestamp', 0)
        ads_viewed_data.append((author, time))

    return ads_viewed_data

# Function to write the results to a CSV file
def write_to_csv(data, output_csv):
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Company Name", "Number of Ads Viewed"])
        for company, count in data.items():
            writer.writerow([company, count])

# Main function to process the data
def main():
    try:
        ads_viewed_data = extract_ads_viewed(root_dir)
    except FileNotFoundError as e:
        # If the file is not found, create a CSV with only headers
        with open(output_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
        return

    # Aggregate the data
    ads_count = {}
    for company, _ in ads_viewed_data:
        if company in ads_count:
            ads_count[company] += 1
        else:
            ads_count[company] = 1

    # Write the results to the CSV file
    write_to_csv(ads_count, output_csv)

if __name__ == "__main__":
    main()
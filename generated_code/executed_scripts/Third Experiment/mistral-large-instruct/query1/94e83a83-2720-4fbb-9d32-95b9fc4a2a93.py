import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to extract topics of interest
def extract_topics_of_interest(root_dir):
    topics_of_interest = []

    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    # Define the path to the ads_and_topics directory
    ads_and_topics_dir = os.path.join(root_dir, 'ads_information', 'ads_and_topics')

    # Check if the ads_and_topics directory exists
    if not os.path.exists(ads_and_topics_dir):
        raise FileNotFoundError("Error: The ads_and_topics directory does not exist.")

    # Define the path to the ads_viewed.json file
    ads_viewed_file = os.path.join(ads_and_topics_dir, 'ads_viewed.json')

    # Check if the ads_viewed.json file exists
    if not os.path.exists(ads_viewed_file):
        raise FileNotFoundError("Error: The ads_viewed.json file does not exist.")

    # Read the ads_viewed.json file
    try:
        with open(ads_viewed_file, 'r') as file:
            ads_viewed_data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError("Error: The ads_viewed.json file is not a valid JSON.")

    # Extract topics of interest from the ads_viewed.json file
    for ad in ads_viewed_data.get('impressions_history_ads_seen', []):
        author = ad.get('string_map_data', {}).get('Author', {}).get('value', '')
        if author:
            topics_of_interest.append(author)

    return topics_of_interest

# Function to write the results to a CSV file
def write_to_csv(topics_of_interest, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Topics of Interest'])
        for topic in topics_of_interest:
            writer.writerow([topic])

# Main function to execute the script
def main():
    try:
        topics_of_interest = extract_topics_of_interest(root_dir)
        write_to_csv(topics_of_interest, output_csv)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
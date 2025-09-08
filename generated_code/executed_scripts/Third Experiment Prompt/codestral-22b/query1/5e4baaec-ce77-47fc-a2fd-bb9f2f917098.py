import os
import json
import csv

root_dir = "root_dir"

def extract_topics_of_interest(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    topics_of_interest = []

    # Navigate to the 'ads_information' directory
    ads_info_dir = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses')

    # Check if the directory exists
    if os.path.exists(ads_info_dir):
        # Navigate to the 'ads_about_meta.json' file
        ads_about_meta_file = os.path.join(ads_info_dir, 'ads_about_meta.json')

        # Check if the file exists
        if os.path.exists(ads_about_meta_file):
            # Load the JSON data
            with open(ads_about_meta_file, 'r') as f:
                data = json.load(f)

            # Check if the 'structure' key exists
            if 'structure' in data:
                # Extract the topics of interest
                for item in data['structure']['label_values']:
                    if 'value' in item:
                        topics_of_interest.append(item['value'])

    # Navigate to the 'connections' directory
    connections_dir = os.path.join(root_dir, 'connections', 'followers_and_following')

    # Check if the directory exists
    if os.path.exists(connections_dir):
        # Navigate to the 'followers_1.json' file
        followers_file = os.path.join(connections_dir, 'followers_1.json')

        # Check if the file exists
        if os.path.exists(followers_file):
            # Load the JSON data
            with open(followers_file, 'r') as f:
                data = json.load(f)

            # Extract the topics of interest
            for item in data:
                for string_data in item['string_list_data']:
                    if 'value' in string_data:
                        topics_of_interest.append(string_data['value'])

    # Save the results to a CSV file
    with open('query_responses/results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Topics of Interest'])
        for topic in topics_of_interest:
            writer.writerow([topic])

extract_topics_of_interest(root_dir)
import os
import csv

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize an empty list to store topics of interest
        topics_of_interest = []

        # Check if the 'ads_information' directory exists
        ads_info_dir = os.path.join(root_dir, 'ads_information')
        if os.path.exists(ads_info_dir):
            # Check if the 'ads_and_topics' directory exists
            ads_and_topics_dir = os.path.join(ads_info_dir, 'ads_and_topics')
            if os.path.exists(ads_and_topics_dir):
                # Check if the 'ads_viewed.json' file exists
                ads_viewed_file = os.path.join(ads_and_topics_dir, 'ads_viewed.json')
                if os.path.exists(ads_viewed_file):
                    # Open the 'ads_viewed.json' file and extract topics of interest
                    with open(ads_viewed_file, 'r') as file:
                        # Since the exact structure of the JSON file is not provided, 
                        # we assume it's a simple JSON file with a list of topics
                        import json
                        data = json.load(file)
                        for item in data['impressions_history_ads_seen']:
                            if 'string_map_data' in item and 'Author' in item['string_map_data']:
                                topics_of_interest.append(item['string_map_data']['Author']['value'])

        # Save the topics of interest to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Topics of Interest']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for topic in topics_of_interest:
                writer.writerow({'Topics of Interest': topic})

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")

    except Exception as e:
        raise ValueError(f"Error: {e}")

get_topics_of_interest(root_dir)
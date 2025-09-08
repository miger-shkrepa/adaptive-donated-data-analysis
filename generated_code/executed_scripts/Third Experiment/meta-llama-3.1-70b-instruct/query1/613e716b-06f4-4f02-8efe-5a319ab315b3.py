import os
import json
import csv

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize an empty set to store unique topics of interest
        topics_of_interest = set()

        # Check if the 'ads_information' directory exists
        ads_info_dir = os.path.join(root_dir, 'ads_information')
        if os.path.exists(ads_info_dir):
            # Check if the 'ads_and_topics' directory exists
            ads_and_topics_dir = os.path.join(ads_info_dir, 'ads_and_topics')
            if os.path.exists(ads_and_topics_dir):
                # Check if the 'in-app_message.json' file exists
                in_app_message_file = os.path.join(ads_and_topics_dir, 'in-app_message.json')
                if os.path.exists(in_app_message_file):
                    with open(in_app_message_file, 'r') as file:
                        data = json.load(file)
                        for item in data['impressions_history_app_message']:
                            for key, value in item['string_map_data'].items():
                                if key == 'In-app message name':
                                    topics_of_interest.add(value['value'])

        # Check if the 'logged_information' directory exists
        logged_info_dir = os.path.join(root_dir, 'logged_information')
        if os.path.exists(logged_info_dir):
            # Check if the 'recent_searches' directory exists
            recent_searches_dir = os.path.join(logged_info_dir, 'recent_searches')
            if os.path.exists(recent_searches_dir):
                # Check if the 'profile_searches.json' file exists
                profile_searches_file = os.path.join(recent_searches_dir, 'profile_searches.json')
                if os.path.exists(profile_searches_file):
                    with open(profile_searches_file, 'r') as file:
                        data = json.load(file)
                        for item in data['searches_user']:
                            for key, value in item['string_map_data'].items():
                                if key == 'Search':
                                    topics_of_interest.add(value['value'])

        return topics_of_interest

    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_to_csv(topics_of_interest):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Topics of Interest'])
            for topic in topics_of_interest:
                writer.writerow([topic])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        topics_of_interest = get_topics_of_interest(root_dir)
        if topics_of_interest:
            write_to_csv(topics_of_interest)
        else:
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Topics of Interest'])
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()
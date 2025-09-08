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
                # Check if the 'accounts_you're_not_interested_in.json' file exists
                accounts_not_interested_file = os.path.join(ads_and_topics_dir, 'accounts_you\'re_not_interested_in.json')
                if os.path.exists(accounts_not_interested_file):
                    # Open the 'accounts_you're_not_interested_in.json' file and read its content
                    with open(accounts_not_interested_file, 'r') as file:
                        # Since the exact structure of the JSON file is not provided, 
                        # we assume it contains a list of topics of interest
                        # and we append them to the 'topics_of_interest' list
                        # For the purpose of this example, we will assume the JSON file contains a list of strings
                        import json
                        data = json.load(file)
                        for item in data['impressions_history_recs_hidden_authors']:
                            topics_of_interest.append(item['title'])

        # Write the topics of interest to a CSV file
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
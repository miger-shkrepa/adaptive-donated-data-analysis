import os
import json
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
        ads_information_dir = os.path.join(root_dir, 'ads_information')
        if os.path.exists(ads_information_dir):
            # Check if the 'ad_preferences.json' file exists
            ad_preferences_file = os.path.join(ads_information_dir, 'instagram_ads_and_businesses', 'ad_preferences.json')
            if os.path.exists(ad_preferences_file):
                # Open and read the 'ad_preferences.json' file
                with open(ad_preferences_file, 'r') as file:
                    ad_preferences_data = json.load(file)

                # Extract topics of interest from the 'ad_preferences.json' file
                for label_value in ad_preferences_data['label_values']:
                    if 'label' in label_value and 'value' in label_value:
                        topics_of_interest.append(label_value['value'])

        # Return the list of topics of interest
        return topics_of_interest

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_topics_of_interest_to_csv(topics_of_interest):
    try:
        # Create the 'query_responses' directory if it does not exist
        query_responses_dir = 'query_responses'
        if not os.path.exists(query_responses_dir):
            os.makedirs(query_responses_dir)

        # Save the topics of interest to a CSV file
        with open(os.path.join(query_responses_dir, 'results.csv'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Topics of Interest'])
            for topic in topics_of_interest:
                writer.writerow([topic])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        topics_of_interest = get_topics_of_interest(root_dir)
        save_topics_of_interest_to_csv(topics_of_interest)

    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: " + str(e))
    except ValueError as e:
        raise ValueError("Error: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()
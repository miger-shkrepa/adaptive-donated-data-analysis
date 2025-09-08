import os
import csv

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize topics of interest
        topics_of_interest = []

        # Define the path to the 'locations_of_interest.json' file
        locations_of_interest_path = os.path.join(root_dir, 'personal_information', 'information_about_you', 'locations_of_interest.json')

        # Check if the 'locations_of_interest.json' file exists
        if os.path.exists(locations_of_interest_path):
            # Open the 'locations_of_interest.json' file
            with open(locations_of_interest_path, 'r') as file:
                # Read the contents of the file
                import json
                data = json.load(file)

                # Extract the topics of interest
                for label_value in data.get('label_values', []):
                    topic = label_value.get('label')
                    if topic:
                        topics_of_interest.append(topic)

        # Define the path to the 'other_categories_used_to_reach_you.json' file
        other_categories_path = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'other_categories_used_to_reach_you.json')

        # Check if the 'other_categories_used_to_reach_you.json' file exists
        if os.path.exists(other_categories_path):
            # Open the 'other_categories_used_to_reach_you.json' file
            with open(other_categories_path, 'r') as file:
                # Read the contents of the file
                import json
                data = json.load(file)

                # Extract the topics of interest
                for label_value in data.get('label_values', []):
                    topic = label_value.get('label')
                    if topic:
                        topics_of_interest.append(topic)

        return topics_of_interest

    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_topics_to_csv(topics_of_interest):
    try:
        # Define the path to the output CSV file
        output_path = 'query_responses/results.csv'

        # Create the output directory if it does not exist
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Write the topics of interest to the CSV file
        with open(output_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Topics of Interest'])
            for topic in topics_of_interest:
                writer.writerow([topic])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        topics_of_interest = get_topics_of_interest(root_dir)
        write_topics_to_csv(topics_of_interest)
    except FileNotFoundError as e:
        # If the root directory does not exist, write an empty CSV file
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Topics of Interest'])
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()
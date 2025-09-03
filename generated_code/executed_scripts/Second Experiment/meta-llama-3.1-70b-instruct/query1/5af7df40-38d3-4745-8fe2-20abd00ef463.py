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

        # Check if the 'information_about_you' directory exists
        information_about_you_dir = os.path.join(root_dir, 'information_about_you')
        if os.path.exists(information_about_you_dir):
            # Check if the 'locations_of_interest.json' file exists
            locations_of_interest_file = os.path.join(information_about_you_dir, 'locations_of_interest.json')
            if os.path.exists(locations_of_interest_file):
                # Open and read the 'locations_of_interest.json' file
                with open(locations_of_interest_file, 'r') as file:
                    # Since we don't have the actual JSON data, we'll assume it's a valid JSON file
                    # and that the 'label_values' key contains the topics of interest
                    import json
                    data = json.load(file)
                    if 'label_values' in data:
                        for label_value in data['label_values']:
                            if 'label' in label_value:
                                topics_of_interest.append(label_value['label'])
                            elif 'value' in label_value:
                                topics_of_interest.append(label_value['value'])

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
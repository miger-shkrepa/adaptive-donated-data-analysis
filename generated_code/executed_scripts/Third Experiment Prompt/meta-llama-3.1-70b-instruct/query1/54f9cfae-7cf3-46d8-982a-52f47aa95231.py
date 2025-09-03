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
            # Open and read the 'locations_of_interest.json' file
            with open(locations_of_interest_path, 'r') as file:
                # Since the structure of the 'locations_of_interest.json' file is not provided, 
                # we assume it's a list of labels
                import json
                data = json.load(file)
                for label_value in data['label_values']:
                    if 'value' in label_value:
                        topics_of_interest.append(label_value['value'])

        # Define the path to the 'recommended_topics.json' file
        recommended_topics_path = os.path.join(root_dir, 'preferences', 'your_topics', 'recommended_topics.json')

        # Check if the 'recommended_topics.json' file exists
        if os.path.exists(recommended_topics_path):
            # Open and read the 'recommended_topics.json' file
            with open(recommended_topics_path, 'r') as file:
                import json
                data = json.load(file)
                for topic in data['topics_your_topics']:
                    if 'string_map_data' in topic and 'Name' in topic['string_map_data']:
                        topics_of_interest.append(topic['string_map_data']['Name']['value'])

        return topics_of_interest

    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_topics_to_csv(topics_of_interest):
    try:
        # Define the path to the output CSV file
        output_path = 'query_responses/results.csv'

        # Create the 'query_responses' directory if it does not exist
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
        raise FileNotFoundError("FileNotFoundError: " + str(e))
    except ValueError as e:
        raise ValueError("Error: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()
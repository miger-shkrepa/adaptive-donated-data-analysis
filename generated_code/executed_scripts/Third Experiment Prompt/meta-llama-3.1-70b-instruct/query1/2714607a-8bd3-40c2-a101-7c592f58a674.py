import os
import csv
import json

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize an empty list to store topics of interest
        topics_of_interest = []

        # Define the path to the 'your_topics.json' file
        your_topics_path = os.path.join(root_dir, 'preferences', 'your_topics', 'your_topics.json')

        # Check if the 'your_topics.json' file exists
        if os.path.exists(your_topics_path):
            # Open the 'your_topics.json' file and read its contents
            with open(your_topics_path, 'r') as file:
                # Load the JSON data
                data = json.load(file)
                for topic in data['topics_your_topics']:
                    # Extract the topic name from the JSON data
                    topic_name = topic['string_map_data']['Name']['value']
                    topics_of_interest.append(topic_name)
        else:
            # If the 'your_topics.json' file does not exist, return an empty list
            pass

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
            writer.writerow(["Topics of Interest"])  # Write the header
            for topic in topics_of_interest:
                writer.writerow([topic])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        topics_of_interest = get_topics_of_interest(root_dir)
        write_topics_to_csv(topics_of_interest)
    except Exception as e:
        # If an error occurs, write an empty CSV file with the header
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Topics of Interest"])
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()
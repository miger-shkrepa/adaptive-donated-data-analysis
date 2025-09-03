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

        # Define the path to the 'your_topics.json' file
        your_topics_path = os.path.join(root_dir, 'preferences', 'your_topics', 'your_topics.json')

        # Check if the 'your_topics.json' file exists
        if os.path.exists(your_topics_path):
            # Open the 'your_topics.json' file
            with open(your_topics_path, 'r') as file:
                # Read the contents of the file
                import json
                data = json.load(file)

                # Extract the topics of interest
                for topic in data['topics_your_topics']:
                    topics_of_interest.append(topic['title'])

        # Return the topics of interest
        return topics_of_interest

    except Exception as e:
        # Raise an exception with a meaningful error message
        raise ValueError("Error: " + str(e))

def write_topics_to_csv(topics_of_interest):
    try:
        # Define the path to the output CSV file
        output_path = 'query_responses/results.csv'

        # Create the 'query_responses' directory if it does not exist
        if not os.path.exists('query_responses'):
            os.makedirs('query_responses')

        # Open the output CSV file
        with open(output_path, 'w', newline='') as file:
            # Create a CSV writer
            writer = csv.writer(file)

            # Write the header
            writer.writerow(['Topics of Interest'])

            # Write the topics of interest
            for topic in topics_of_interest:
                writer.writerow([topic])

    except Exception as e:
        # Raise an exception with a meaningful error message
        raise ValueError("Error: " + str(e))

def main():
    try:
        # Get the topics of interest
        topics_of_interest = get_topics_of_interest(root_dir)

        # Write the topics of interest to a CSV file
        write_topics_to_csv(topics_of_interest)

    except Exception as e:
        # Write an empty CSV file if an error occurs
        output_path = 'query_responses/results.csv'
        if not os.path.exists('query_responses'):
            os.makedirs('query_responses')
        with open(output_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Topics of Interest'])
        print("Error: " + str(e))

if __name__ == "__main__":
    main()
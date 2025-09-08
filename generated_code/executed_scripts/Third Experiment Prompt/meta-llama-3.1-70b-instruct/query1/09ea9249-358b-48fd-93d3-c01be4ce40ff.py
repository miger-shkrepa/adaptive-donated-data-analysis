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

        # Define the path to the 'recommended_topics.json' file
        recommended_topics_path = os.path.join(root_dir, 'preferences', 'your_topics', 'recommended_topics.json')

        # Check if the 'recommended_topics.json' file exists
        if os.path.exists(recommended_topics_path):
            # Open the 'recommended_topics.json' file
            with open(recommended_topics_path, 'r') as file:
                # Read the contents of the file
                import json
                data = json.load(file)

                # Extract the topics of interest
                for topic in data['topics_your_topics']:
                    topics_of_interest.append(topic['string_map_data']['Name']['value'])

        # Return the topics of interest
        return topics_of_interest

    except Exception as e:
        # Raise an exception with a meaningful error message
        raise ValueError("Error: " + str(e))

def write_topics_to_csv(topics_of_interest):
    try:
        # Define the path to the output CSV file
        output_path = 'query_responses/results.csv'

        # Create the output directory if it does not exist
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

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

    except FileNotFoundError as e:
        # If the root directory does not exist, write an empty CSV file
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Topics of Interest'])
        print(e)
    except Exception as e:
        # Raise an exception with a meaningful error message
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()
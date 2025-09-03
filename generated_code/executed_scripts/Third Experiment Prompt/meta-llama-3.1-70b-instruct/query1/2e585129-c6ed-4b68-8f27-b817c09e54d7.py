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
            try:
                # Open and read the 'your_topics.json' file
                with open(your_topics_path, 'r') as file:
                    # Load the JSON data
                    import json
                    data = json.load(file)

                    # Extract the topics of interest
                    for topic in data['topics_your_topics']:
                        topics_of_interest.append(topic['string_map_data']['Name']['value'])

            except Exception as e:
                raise ValueError("ValueError: Failed to parse 'your_topics.json' file. Error: " + str(e))

        # Return the topics of interest
        return topics_of_interest

    except Exception as e:
        raise Exception("Error: " + str(e))

def save_topics_to_csv(topics_of_interest):
    try:
        # Define the path to the output CSV file
        output_path = 'query_responses/results.csv'

        # Create the output directory if it does not exist
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the topics of interest to the CSV file
        with open(output_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Topics of Interest'])
            for topic in topics_of_interest:
                writer.writerow([topic])

    except Exception as e:
        raise Exception("Error: Failed to save topics to CSV file. Error: " + str(e))

def main():
    try:
        topics_of_interest = get_topics_of_interest(root_dir)
        save_topics_to_csv(topics_of_interest)

    except FileNotFoundError as e:
        # If the root directory does not exist, save a CSV file with only the column headers
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Topics of Interest'])
        print(e)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
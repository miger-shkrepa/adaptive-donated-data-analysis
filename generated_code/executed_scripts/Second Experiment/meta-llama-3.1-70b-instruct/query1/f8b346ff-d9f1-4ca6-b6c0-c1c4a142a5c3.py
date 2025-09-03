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
                    # Since we don't know the exact structure of the JSON file, we'll assume it's a list of labels
                    # and extract the labels
                    import json
                    data = json.load(file)
                    for label_value in data.get('label_values', []):
                        label = label_value.get('label')
                        if label:
                            topics_of_interest.append(label)

        # Return the topics of interest
        return topics_of_interest

    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_topics_to_csv(topics_of_interest):
    try:
        # Create the 'query_responses' directory if it doesn't exist
        query_responses_dir = 'query_responses'
        if not os.path.exists(query_responses_dir):
            os.makedirs(query_responses_dir)

        # Write the topics of interest to a CSV file
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
        write_topics_to_csv(topics_of_interest)
    except FileNotFoundError as e:
        # If the root directory or a required file does not exist, write a CSV file with only the column headers
        with open(os.path.join('query_responses', 'results.csv'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Topics of Interest'])
        print(e)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
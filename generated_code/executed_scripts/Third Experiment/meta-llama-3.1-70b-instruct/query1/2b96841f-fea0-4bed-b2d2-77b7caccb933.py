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

        # Iterate over all files and directories in the root directory
        for dir_path, dir_names, file_names in os.walk(root_dir):
            # Check if the 'media' directory exists
            if 'media' in dir_names:
                media_dir = os.path.join(dir_path, 'media')
                # Check if the 'stories.json' file exists in the 'media' directory
                if os.path.exists(os.path.join(media_dir, 'stories.json')):
                    # Open the 'stories.json' file and read its contents
                    with open(os.path.join(media_dir, 'stories.json'), 'r') as file:
                        # Since we don't have the actual JSON data, we'll assume it's in the correct format
                        # and that we can parse it correctly
                        import json
                        data = json.load(file)
                        # Iterate over the 'ig_stories' list
                        for story in data['ig_stories']:
                            # Check if the 'media_metadata' key exists
                            if 'media_metadata' in story:
                                # Check if the 'interest_topics' key exists
                                if 'interest_topics' in story['media_metadata']:
                                    # Iterate over the 'interest_topics' list
                                    for topic in story['media_metadata']['interest_topics']:
                                        # Append the topic name to the list of topics of interest
                                        topics_of_interest.append(topic['topic_name'])

        # Return the list of topics of interest
        return topics_of_interest

    except Exception as e:
        # Raise a ValueError with the error message
        raise ValueError("Error: " + str(e))

def write_to_csv(topics_of_interest):
    try:
        # Open the 'results.csv' file in write mode
        with open('query_responses/results.csv', 'w', newline='') as file:
            # Create a CSV writer
            writer = csv.writer(file)
            # Write the column header
            writer.writerow(['Topics of Interest'])
            # Write each topic of interest
            for topic in topics_of_interest:
                writer.writerow([topic])

    except Exception as e:
        # Raise a ValueError with the error message
        raise ValueError("Error: " + str(e))

def main():
    try:
        # Get the topics of interest
        topics_of_interest = get_topics_of_interest(root_dir)
        # Write the topics of interest to the 'results.csv' file
        write_to_csv(topics_of_interest)

    except FileNotFoundError as e:
        # If the root directory does not exist, write an empty CSV file
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Topics of Interest'])
        print(e)

    except Exception as e:
        # Raise a ValueError with the error message
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()
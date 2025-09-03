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

        # Iterate over all files in the root directory
        for filename in os.listdir(root_dir):
            # Check if the file is 'reels.json'
            if filename == 'reels.json':
                # Open the 'reels.json' file
                with open(os.path.join(root_dir, filename), 'r') as file:
                    # Read the contents of the file
                    contents = file.read()

                    # Check if the file contains the required structure
                    if 'ig_reels_media' in contents and 'media' in contents and 'interest_topics' in contents:
                        # Extract the topics of interest
                        import json
                        data = json.loads(contents)
                        for media in data['ig_reels_media']:
                            for item in media['media']:
                                if 'interest_topics' in item:
                                    for topic in item['interest_topics']:
                                        topics_of_interest.append(topic['topic_name'])

        # Return the topics of interest
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

            # Write the topics of interest
            for topic in topics_of_interest:
                writer.writerow([topic])

    except Exception as e:
        # Raise a ValueError with the error message
        raise ValueError("Error: " + str(e))

def main():
    try:
        # Get the topics of interest
        topics_of_interest = get_topics_of_interest(root_dir)

        # Check if the topics of interest are empty
        if not topics_of_interest:
            # Write an empty CSV file with only the column header
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Topics of Interest'])
        else:
            # Write the topics of interest to the CSV file
            write_to_csv(topics_of_interest)

    except Exception as e:
        # Raise a ValueError with the error message
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()
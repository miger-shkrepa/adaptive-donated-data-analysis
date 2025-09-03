import os
import csv

root_dir = "root_dir"

def get_user_engagement(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a dictionary to store user engagement
        user_engagement = {}

        # Iterate over the 'messages' directory
        messages_dir = os.path.join(root_dir, 'messages')
        if os.path.exists(messages_dir):
            for username in os.listdir(messages_dir):
                username_path = os.path.join(messages_dir, username)
                if os.path.isdir(username_path):
                    for filename in os.listdir(username_path):
                        if filename.endswith('.json'):
                            file_path = os.path.join(username_path, filename)
                            try:
                                # Open the JSON file and count the reactions
                                with open(file_path, 'r') as file:
                                    data = eval(file.read())
                                    for message in data['messages']:
                                        if 'reactions' in message:
                                            for reaction in message['reactions']:
                                                actor = reaction['actor']
                                                if actor not in user_engagement:
                                                    user_engagement[actor] = 1
                                                else:
                                                    user_engagement[actor] += 1
                            except Exception as e:
                                raise ValueError("ValueError: Failed to parse JSON file: " + str(e))

        # Create a CSV file with the user engagement data
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['User', 'Times Engaged']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            if user_engagement:
                for user, engagement in user_engagement.items():
                    writer.writerow({'User': user, 'Times Engaged': engagement})
            else:
                # If no engagement data is found, write only the column headers
                writer.writeheader()

    except Exception as e:
        raise Exception("Error: " + str(e))

get_user_engagement(root_dir)
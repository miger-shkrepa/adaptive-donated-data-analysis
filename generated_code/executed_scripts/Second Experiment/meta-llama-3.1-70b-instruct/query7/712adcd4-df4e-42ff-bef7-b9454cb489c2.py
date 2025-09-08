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
                                # Open and read the JSON file
                                with open(file_path, 'r') as file:
                                    # Since we don't have the actual JSON data, we'll assume it's a list of messages
                                    # and each message has a 'sender_name' and 'reactions' field
                                    messages = eval(file.read())
                                    for message in messages['messages']:
                                        if 'sender_name' in message:
                                            sender = message['sender_name']
                                            if sender not in user_engagement:
                                                user_engagement[sender] = 0
                                            if 'reactions' in message:
                                                user_engagement[sender] += len(message['reactions'])
                            except Exception as e:
                                raise ValueError("ValueError: Failed to parse JSON file: " + str(e))

        # Create a CSV file with the user engagement data
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['User', 'Times Engaged']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for user, engagement in user_engagement.items():
                writer.writerow({'User': user, 'Times Engaged': engagement})

    except Exception as e:
        # If any error occurs, create a CSV file with only the column headers
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['User', 'Times Engaged']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        raise Exception("Error: " + str(e))

get_user_engagement(root_dir)
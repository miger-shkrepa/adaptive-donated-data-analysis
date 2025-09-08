import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Function to process the directory and extract relevant data
def process_directory(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    user_engagement = {}

    # Define the path to the connections directory
    connections_dir = os.path.join(root_dir, "connections")

    # Check if the connections directory exists
    if not os.path.exists(connections_dir):
        raise FileNotFoundError("Error: The connections directory does not exist.")

    # Define the path to the followers_and_following directory
    followers_and_following_dir = os.path.join(connections_dir, "followers_and_following")

    # Check if the followers_and_following directory exists
    if not os.path.exists(followers_and_following_dir):
        raise FileNotFoundError("Error: The followers_and_following directory does not exist.")

    # Define the path to the close_friends.json file
    close_friends_file = os.path.join(followers_and_following_dir, "close_friends.json")

    # Check if the close_friends.json file exists
    if not os.path.exists(close_friends_file):
        raise FileNotFoundError("Error: The close_friends.json file does not exist.")

    # Read the close_friends.json file
    with open(close_friends_file, 'r') as file:
        close_friends_data = json.load(file)

    # Extract user engagement data
    for entry in close_friends_data.get("relationships_close_friends", []):
        for user in entry.get("string_list_data", []):
            user_name = user.get("value", "")
            if user_name:
                if user_name not in user_engagement:
                    user_engagement[user_name] = 0
                user_engagement[user_name] += 1

    # Write the results to a CSV file
    output_file = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['User', 'Times Engaged']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for user, times_engaged in user_engagement.items():
            writer.writerow({'User': user, 'Times Engaged': times_engaged})

# Call the function to process the directory
process_directory(root_dir)
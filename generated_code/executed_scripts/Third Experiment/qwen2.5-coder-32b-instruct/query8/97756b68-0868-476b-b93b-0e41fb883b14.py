import os
import csv
from collections import defaultdict

# Variable referring to the file input
root_dir = "root_dir"

# Function to check if a directory exists
def check_directory_exists(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError(f"FileNotFoundError: The directory {directory} does not exist.")

# Function to check if a file exists
def check_file_exists(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")

# Function to read JSON files and extract relevant data
def read_json_file(file_path):
    import json
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Function to process messages and extract interactions
def process_messages(messages):
    interactions = defaultdict(int)
    for message in messages:
        if 'sender_name' in message:
            interactions[message['sender_name']] += 1
    return interactions

# Main function to gather interactions
def gather_interactions(root_dir):
    interactions = defaultdict(int)
    
    # Check if the root directory exists
    check_directory_exists(root_dir)
    
    # Check for the 'messages' directory
    messages_dir = os.path.join(root_dir, 'messages')
    if os.path.exists(messages_dir):
        for user_dir in os.listdir(messages_dir):
            user_path = os.path.join(messages_dir, user_dir)
            if os.path.isdir(user_path):
                for file_name in os.listdir(user_path):
                    if file_name.endswith('.json'):
                        file_path = os.path.join(user_path, file_name)
                        try:
                            data = read_json_file(file_path)
                            if 'messages' in data['message_1.json']['structure']:
                                user_interactions = process_messages(data['message_1.json']['structure']['messages'])
                                for user, count in user_interactions.items():
                                    interactions[user] += count
                        except Exception as e:
                            print(f"Error processing file {file_path}: {e}")
    
    return interactions

# Function to write interactions to CSV
def write_interactions_to_csv(interactions, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['User', 'Post Likes', 'Story Likes and Comments'])
        for user, count in sorted(interactions.items(), key=lambda item: item[1], reverse=True)[:20]:
            writer.writerow([user, 0, count])  # Assuming all interactions are story likes and comments

# Main execution
try:
    interactions = gather_interactions(root_dir)
    write_interactions_to_csv(interactions, 'query_responses/results.csv')
except FileNotFoundError as e:
    print(e)
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['User', 'Post Likes', 'Story Likes and Comments'])
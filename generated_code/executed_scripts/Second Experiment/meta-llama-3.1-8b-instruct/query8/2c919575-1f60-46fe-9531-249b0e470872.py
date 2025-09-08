import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the dictionary to store the user interactions
user_interactions = {}

# Function to process the JSON files
def process_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            # Assuming the JSON data is in the format of a list of dictionaries
            for item in eval(data):
                # Assuming the 'title' key corresponds to the user's name
                user = item['title']
                # Assuming the 'string_list_data' key corresponds to the post likes
                post_likes = len(item.get('string_list_data', []))
                # Assuming the 'string_list_data' key corresponds to the story likes
                story_likes = len(item.get('string_list_data', []))
                # Assuming the 'string_list_data' key corresponds to the comments
                comments = len(item.get('string_list_data', []))
                # Update the user interactions dictionary
                user_interactions[user] = user_interactions.get(user, [0, 0, 0])
                user_interactions[user][0] += post_likes
                user_interactions[user][1] += story_likes
                user_interactions[user][2] += comments
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")

# Function to process the JSON files in the 'likes' directory
def process_likes_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            # Assuming the JSON data is in the format of a list of dictionaries
            for item in eval(data):
                # Assuming the 'title' key corresponds to the user's name
                user = item['title']
                # Assuming the 'string_list_data' key corresponds to the post likes
                post_likes = len(item.get('string_list_data', []))
                # Update the user interactions dictionary
                user_interactions[user] = user_interactions.get(user, [0, 0, 0])
                user_interactions[user][0] += post_likes
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")

# Function to process the JSON files in the 'messages' directory
def process_messages_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            # Assuming the JSON data is in the format of a list of dictionaries
            for item in eval(data):
                # Assuming the 'sender_name' key corresponds to the user's name
                user = item['sender_name']
                # Assuming the 'reactions' key corresponds to the comments
                comments = len(item.get('reactions', []))
                # Update the user interactions dictionary
                user_interactions[user] = user_interactions.get(user, [0, 0, 0])
                user_interactions[user][2] += comments
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")

# Process the JSON files in the 'likes' directory
likes_dir = os.path.join(root_dir, 'likes')
if os.path.exists(likes_dir):
    for file in os.listdir(likes_dir):
        if file.endswith('.json'):
            process_likes_json_file(os.path.join(likes_dir, file))

# Process the JSON files in the 'messages' directory
messages_dir = os.path.join(root_dir, 'messages')
if os.path.exists(messages_dir):
    for file in os.listdir(messages_dir):
        if file.endswith('.json'):
            process_messages_json_file(os.path.join(messages_dir, file))

# Process the JSON files in the 'personal_information' directory
personal_info_dir = os.path.join(root_dir, 'personal_information')
if os.path.exists(personal_info_dir):
    for file in os.listdir(personal_info_dir):
        if file.endswith('.json'):
            process_json_file(os.path.join(personal_info_dir, file))

# Sort the user interactions dictionary by the sum of post likes, story likes, and comments
sorted_user_interactions = dict(sorted(user_interactions.items(), key=lambda item: sum(item[1]), reverse=True))

# Write the sorted user interactions to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
    for user, interactions in sorted_user_interactions.items():
        writer.writerow([user, interactions[0], interactions[1], interactions[2]])
        if len(sorted_user_interactions) > 20:
            break
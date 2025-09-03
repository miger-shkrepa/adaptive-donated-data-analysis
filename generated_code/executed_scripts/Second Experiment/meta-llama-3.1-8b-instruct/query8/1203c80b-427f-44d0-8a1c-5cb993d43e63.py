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
                # Assuming the 'title' key contains the user name
                user = item['title']
                # Assuming the 'string_list_data' key contains the post likes
                post_likes = len(item['string_list_data'])
                # Assuming the 'string_list_data' key contains the story likes
                story_likes = len(item['string_list_data'])
                # Assuming the 'string_list_data' key contains the comments
                comments = len(item['string_list_data'])
                # Update the user interactions dictionary
                if user in user_interactions:
                    user_interactions[user]['post_likes'] += post_likes
                    user_interactions[user]['story_likes'] += story_likes
                    user_interactions[user]['comments'] += comments
                else:
                    user_interactions[user] = {'post_likes': post_likes, 'story_likes': story_likes, 'comments': comments}
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")

# Function to process the JSON files in the 'likes' directory
def process_likes_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            # Assuming the JSON data is in the format of a list of dictionaries
            for item in eval(data):
                # Assuming the 'title' key contains the user name
                user = item['title']
                # Assuming the 'string_list_data' key contains the post likes
                post_likes = len(item['string_list_data'])
                # Update the user interactions dictionary
                if user in user_interactions:
                    user_interactions[user]['post_likes'] += post_likes
                else:
                    user_interactions[user] = {'post_likes': post_likes, 'story_likes': 0, 'comments': 0}
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")

# Function to process the JSON files in the 'messages' directory
def process_messages_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            # Assuming the JSON data is in the format of a list of dictionaries
            for item in eval(data):
                # Assuming the 'sender_name' key contains the user name
                user = item['sender_name']
                # Assuming the 'reactions' key contains the story likes
                story_likes = len(item['reactions'])
                # Assuming the 'reactions' key contains the comments
                comments = len(item['reactions'])
                # Update the user interactions dictionary
                if user in user_interactions:
                    user_interactions[user]['story_likes'] += story_likes
                    user_interactions[user]['comments'] += comments
                else:
                    user_interactions[user] = {'post_likes': 0, 'story_likes': story_likes, 'comments': comments}
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")

# Process the JSON files in the 'likes' directory
likes_dir = os.path.join(root_dir, 'likes')
if os.path.exists(likes_dir):
    for file in os.listdir(likes_dir):
        if file.endswith('.json'):
            file_path = os.path.join(likes_dir, file)
            process_likes_json_file(file_path)

# Process the JSON files in the 'messages' directory
messages_dir = os.path.join(root_dir, 'messages')
if os.path.exists(messages_dir):
    for file in os.listdir(messages_dir):
        if file.endswith('.json'):
            file_path = os.path.join(messages_dir, file)
            process_messages_json_file(file_path)

# Process the JSON files in the 'personal_information' directory
personal_info_dir = os.path.join(root_dir, 'personal_information')
if os.path.exists(personal_info_dir):
    for file in os.listdir(personal_info_dir):
        if file.endswith('.json'):
            file_path = os.path.join(personal_info_dir, file)
            process_json_file(file_path)

# Sort the user interactions by the total interactions in descending order
sorted_users = sorted(user_interactions.items(), key=lambda x: sum(x[1].values()), reverse=True)

# Write the sorted user interactions to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
    for user, interactions in sorted_users[:20]:
        writer.writerow([user, interactions['post_likes'], interactions['story_likes'], interactions['comments']])
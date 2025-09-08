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
                # Assuming the 'likes_media_likes' key exists in the dictionary
                if 'likes_media_likes' in item:
                    for interaction in item['likes_media_likes']:
                        # Assuming the 'string_list_data' key exists in the dictionary
                        if 'string_list_data' in interaction:
                            for value in interaction['string_list_data']:
                                # Assuming the 'value' key exists in the dictionary
                                if 'value' in value:
                                    user = value['value']
                                    if user in user_interactions:
                                        user_interactions[user]['post_likes'] += 1
                                    else:
                                        user_interactions[user] = {'post_likes': 1, 'story_likes': 0, 'comments': 0}
                        # Assuming the 'string_list_data' key exists in the dictionary
                        if 'string_list_data' in interaction:
                            for value in interaction['string_list_data']:
                                # Assuming the 'value' key exists in the dictionary
                                if 'value' in value:
                                    user = value['value']
                                    if user in user_interactions:
                                        user_interactions[user]['story_likes'] += 1
                                    else:
                                        user_interactions[user] = {'post_likes': 0, 'story_likes': 1, 'comments': 0}
                        # Assuming the 'string_list_data' key exists in the dictionary
                        if 'string_list_data' in interaction:
                            for value in interaction['string_list_data']:
                                # Assuming the 'value' key exists in the dictionary
                                if 'value' in value:
                                    user = value['value']
                                    if user in user_interactions:
                                        user_interactions[user]['comments'] += 1
                                    else:
                                        user_interactions[user] = {'post_likes': 0, 'story_likes': 0, 'comments': 1}
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")

# Function to process the JSON files in the 'likes' directory
def process_likes_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            # Assuming the JSON data is in the format of a list of dictionaries
            for item in eval(data):
                # Assuming the 'likes_media_likes' key exists in the dictionary
                if 'likes_media_likes' in item:
                    for interaction in item['likes_media_likes']:
                        # Assuming the 'string_list_data' key exists in the dictionary
                        if 'string_list_data' in interaction:
                            for value in interaction['string_list_data']:
                                # Assuming the 'value' key exists in the dictionary
                                if 'value' in value:
                                    user = value['value']
                                    if user in user_interactions:
                                        user_interactions[user]['post_likes'] += 1
                                    else:
                                        user_interactions[user] = {'post_likes': 1, 'story_likes': 0, 'comments': 0}
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")

# Function to process the JSON files in the 'messages' directory
def process_messages_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            # Assuming the JSON data is in the format of a list of dictionaries
            for item in eval(data):
                # Assuming the 'participants' key exists in the dictionary
                if 'participants' in item:
                    for participant in item['participants']:
                        # Assuming the 'name' key exists in the dictionary
                        if 'name' in participant:
                            user = participant['name']
                            if user in user_interactions:
                                user_interactions[user]['comments'] += 1
                            else:
                                user_interactions[user] = {'post_likes': 0, 'story_likes': 0, 'comments': 1}
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")

# Function to process the JSON files in the 'personal_information' directory
def process_personal_information_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            # Assuming the JSON data is in the format of a list of dictionaries
            for item in eval(data):
                # Assuming the 'profile_user' key exists in the dictionary
                if 'profile_user' in item:
                    for user in item['profile_user']:
                        # Assuming the 'string_map_data' key exists in the dictionary
                        if 'string_map_data' in user:
                            for value in user['string_map_data'].values():
                                # Assuming the 'value' key exists in the dictionary
                                if 'value' in value:
                                    user = value['value']
                                    if user in user_interactions:
                                        user_interactions[user]['comments'] += 1
                                    else:
                                        user_interactions[user] = {'post_likes': 0, 'story_likes': 0, 'comments': 1}
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
personal_information_dir = os.path.join(root_dir, 'personal_information')
if os.path.exists(personal_information_dir):
    for file in os.listdir(personal_information_dir):
        if file.endswith('.json'):
            process_personal_information_json_file(os.path.join(personal_information_dir, file))

# Process the JSON files in the 'events' directory
events_dir = os.path.join(root_dir, 'events')
if os.path.exists(events_dir):
    for file in os.listdir(events_dir):
        if file.endswith('.json'):
            process_json_file(os.path.join(events_dir, file))

# Process the JSON files in the 'information_about_you' directory
information_about_you_dir = os.path.join(root_dir, 'information_about_you')
if os.path.exists(information_about_you_dir):
    for file in os.listdir(information_about_you_dir):
        if file.endswith('.json'):
            process_json_file(os.path.join(information_about_you_dir, file))

# Process the JSON files in the 'media' directory
media_dir = os.path.join(root_dir, 'media')
if os.path.exists(media_dir):
    for file in os.listdir(media_dir):
        if file.endswith('.json'):
            process_json_file(os.path.join(media_dir, file))

# Process the JSON files in the 'personal_information' directory
personal_information_dir = os.path.join(root_dir, 'personal_information')
if os.path.exists(personal_information_dir):
    for file in os.listdir(personal_information_dir):
        if file.endswith('.json'):
            process_json_file(os.path.join(personal_information_dir, file))

# Sort the user interactions by the total number of interactions in descending order
sorted_user_interactions = sorted(user_interactions.items(), key=lambda x: sum(x[1].values()), reverse=True)

# Write the sorted user interactions to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
    for user, interactions in sorted_user_interactions:
        writer.writerow([user, interactions['post_likes'], interactions['story_likes'], interactions['comments']])

print("Query completed successfully.")
import os
import csv
import json

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the interaction counts
interactions = {}

# Function to update the interaction counts
def update_interactions(username, likes, comments):
    if username in interactions:
        interactions[username]['Post Likes'] += likes
        interactions[username]['Comments'] += comments
    else:
        interactions[username] = {'Post Likes': likes, 'Story Likes': 0, 'Comments': comments}

# Traverse the directory structure
for foldername, subfolders, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename == "liked_posts.json":
            filepath = os.path.join(foldername, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                for post in data['likes_media_likes']:
                    username = post['title']
                    likes = len(post['string_list_data'])
                    update_interactions(username, likes, 0)
        elif filename == "event_reminders.json":
            filepath = os.path.join(foldername, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                for event in data['events_event_reminders']:
                    username = event['title']
                    likes = len(event['string_list_data'])
                    update_interactions(username, 0, likes)
        elif filename == "message_1.json":
            filepath = os.path.join(foldername, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                for message in data['messages']:
                    if 'content' in message:
                        username = message['sender_name']
                        update_interactions(username, 0, 1)

# Sort the interactions dictionary by post likes, story likes, and comments
sorted_interactions = sorted(interactions.items(), key=lambda x: (x[1]['Post Likes'], x[1]['Story Likes'], x[1]['Comments']), reverse=True)

# Get the top 20 interactions
top_20_interactions = sorted_interactions[:20]

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
    for user, interaction in top_20_interactions:
        writer.writerow([user, interaction['Post Likes'], interaction['Story Likes'], interaction['Comments']])
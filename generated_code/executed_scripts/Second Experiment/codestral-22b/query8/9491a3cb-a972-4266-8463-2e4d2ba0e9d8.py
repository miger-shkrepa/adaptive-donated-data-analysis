import os
import json
import csv

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
        interactions[username]['Story Likes'] += comments
    else:
        interactions[username] = {'Post Likes': likes, 'Story Likes': comments, 'Comments': 0}

# Process liked posts
liked_posts_path = os.path.join(root_dir, 'likes', 'liked_posts.json')
if os.path.exists(liked_posts_path):
    with open(liked_posts_path, 'r') as f:
        liked_posts = json.load(f)
        for post in liked_posts['structure']['likes_media_likes']:
            username = post['title']
            likes = len(post['string_list_data'])
            update_interactions(username, likes, 0)

# Process event reminders (assuming these are comments)
event_reminders_path = os.path.join(root_dir, 'events', 'event_reminders.json')
if os.path.exists(event_reminders_path):
    with open(event_reminders_path, 'r') as f:
        event_reminders = json.load(f)
        for reminder in event_reminders['structure']['events_event_reminders']:
            username = reminder['title']
            comments = len(reminder['string_list_data'])
            update_interactions(username, 0, comments)

# Sort the interactions dictionary by post likes and story likes
sorted_interactions = sorted(interactions.items(), key=lambda x: (x[1]['Post Likes'], x[1]['Story Likes']), reverse=True)

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
    for username, counts in sorted_interactions[:20]:
        writer.writerow([username, counts['Post Likes'], counts['Story Likes'], counts['Comments']])
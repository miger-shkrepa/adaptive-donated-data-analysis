import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Initialize dictionaries to store interaction counts
post_likes = {}
story_likes = {}
comments = {}

# Helper function to update interaction counts
def update_interaction_counts(data, interaction_type):
    for item in data:
        if interaction_type == 'post_likes':
            for entry in item.get('string_list_data', []):
                user = entry.get('value', '')
                if user:
                    post_likes[user] = post_likes.get(user, 0) + 1
        elif interaction_type == 'story_likes':
            for entry in item.get('string_list_data', []):
                user = entry.get('value', '')
                if user:
                    story_likes[user] = story_likes.get(user, 0) + 1
        elif interaction_type == 'comments':
            for message in item.get('messages', []):
                user = message.get('sender_name', '')
                if user:
                    comments[user] = comments.get(user, 0) + 1

# Process the JSON files
try:
    # Process liked_posts.json
    liked_posts_path = os.path.join(root_dir, 'likes', 'liked_posts.json')
    if os.path.exists(liked_posts_path):
        with open(liked_posts_path, 'r') as file:
            data = json.load(file)
            update_interaction_counts(data.get('likes_media_likes', []), 'post_likes')

    # Process story_likes.json (assuming it exists, adjust path as needed)
    story_likes_path = os.path.join(root_dir, 'likes', 'story_likes.json')
    if os.path.exists(story_likes_path):
        with open(story_likes_path, 'r') as file:
            data = json.load(file)
            update_interaction_counts(data.get('likes_media_likes', []), 'story_likes')

    # Process messages (assuming it exists, adjust path as needed)
    messages_path = os.path.join(root_dir, 'messages', 'inbox', 'username_placeholder', 'message_1.json')
    if os.path.exists(messages_path):
        with open(messages_path, 'r') as file:
            data = json.load(file)
            update_interaction_counts(data.get('messages', []), 'comments')

except FileNotFoundError:
    raise FileNotFoundError("Error: The root directory does not exist.")
except json.JSONDecodeError:
    raise ValueError("Error: Failed to decode JSON.")

# Combine interaction counts
interaction_counts = {}
for user in set(post_likes.keys()).union(story_likes.keys()).union(comments.keys()):
    interaction_counts[user] = {
        'Post Likes': post_likes.get(user, 0),
        'Story Likes': story_likes.get(user, 0),
        'Comments': comments.get(user, 0)
    }

# Sort users by total interactions
sorted_users = sorted(interaction_counts.items(), key=lambda x: sum(x[1].values()), reverse=True)

# Write the results to a CSV file
with open(output_csv, 'w', newline='') as csvfile:
    fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for user, counts in sorted_users[:20]:
        writer.writerow({'User': user, **counts})

print(f"Results saved to {output_csv}")
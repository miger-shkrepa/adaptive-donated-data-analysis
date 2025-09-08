import os
import json
import csv

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the interaction counts
interactions = {}

# Function to update the interaction counts
def update_interactions(user, likes, comments):
    if user not in interactions:
        interactions[user] = {'Post Likes': 0, 'Story Likes': 0, 'Comments': 0}
    interactions[user]['Post Likes'] += likes
    interactions[user]['Story Likes'] += story_likes
    interactions[user]['Comments'] += comments

# Process liked posts
liked_posts_path = os.path.join(root_dir, 'likes', 'liked_posts.json')
if os.path.exists(liked_posts_path):
    with open(liked_posts_path, 'r') as f:
        liked_posts = json.load(f)
    for post in liked_posts['likes_media_likes']:
        user = post['title']
        likes = len(post['string_list_data'])
        update_interactions(user, likes, 0)

# Process story likes
story_likes_path = os.path.join(root_dir, 'story_interactions', 'story_likes.json')
if os.path.exists(story_likes_path):
    with open(story_likes_path, 'r') as f:
        story_likes = json.load(f)
    for story in story_likes['story_activities_story_likes']:
        user = story['title']
        story_likes = len(story['string_list_data'])
        update_interactions(user, 0, story_likes)

# Process liked comments
liked_comments_path = os.path.join(root_dir, 'likes', 'liked_comments.json')
if os.path.exists(liked_comments_path):
    with open(liked_comments_path, 'r') as f:
        liked_comments = json.load(f)
    for comment in liked_comments['likes_comment_likes']:
        user = comment['title']
        comments = len(comment['string_list_data'])
        update_interactions(user, 0, comments)

# Sort the interactions dictionary by total interactions
sorted_interactions = sorted(interactions.items(), key=lambda x: sum(x[1].values()), reverse=True)

# Get the top 20 accounts
top_accounts = sorted_interactions[:20]

# Write the results to a CSV file
output_path = 'query_responses/results.csv'
with open(output_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
    for user, counts in top_accounts:
        writer.writerow([user, counts['Post Likes'], counts['Story Likes'], counts['Comments']])
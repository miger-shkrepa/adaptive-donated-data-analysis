import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize dictionaries to store user interactions
post_likes = {}
story_likes = {}
comments = {}

# Iterate over the directory structure
for dir_path, dir_names, file_names in os.walk(root_dir):
    # Check if the directory contains the 'likes' subdirectory
    if 'likes' in dir_names:
        # Iterate over the files in the 'likes' subdirectory
        for file_name in file_names:
            if file_name == 'liked_posts.json':
                # Parse the 'liked_posts.json' file
                with open(os.path.join(dir_path, file_name), 'r') as file:
                    data = eval(file.read())
                    for post in data['likes_media_likes']:
                        for interaction in post['string_list_data']:
                            user = interaction['value']
                            if user not in post_likes:
                                post_likes[user] = 0
                            post_likes[user] += 1
            elif file_name == 'liked_comments.json':
                # Parse the 'liked_comments.json' file
                with open(os.path.join(dir_path, file_name), 'r') as file:
                    data = eval(file.read())
                    for post in data['likes_comment_likes']:
                        for interaction in post['string_list_data']:
                            user = interaction['value']
                            if user not in comments:
                                comments[user] = 0
                            comments[user] += 1
            elif file_name == 'story_likes.json':
                # Parse the 'story_likes.json' file
                with open(os.path.join(dir_path, file_name), 'r') as file:
                    data = eval(file.read())
                    for story in data['story_activities_story_likes']:
                        for interaction in story['string_list_data']:
                            user = interaction['value']
                            if user not in story_likes:
                                story_likes[user] = 0
                            story_likes[user] += 1

# Sort the users by their total interactions
users = sorted(post_likes.keys(), key=lambda user: post_likes[user] + story_likes.get(user, 0) + comments.get(user, 0), reverse=True)

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
    for user in users[:20]:
        writer.writerow([user, post_likes.get(user, 0), story_likes.get(user, 0), comments.get(user, 0)])
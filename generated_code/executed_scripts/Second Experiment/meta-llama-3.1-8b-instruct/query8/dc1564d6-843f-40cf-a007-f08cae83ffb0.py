import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the counters
post_likes = {}
story_likes = {}
comments = {}

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON file contains the required data
            if 'likes' in data and 'liked_posts.json' in data['likes']:
                # Iterate over the liked posts
                for post in data['likes']['liked_posts.json']['structure']['likes_media_likes']:
                    # Get the user who liked the post
                    user = post['title']

                    # Increment the post likes counter
                    post_likes[user] = post_likes.get(user, 0) + 1

            elif 'personal_information' in data and 'instagram_profile_information.json' in data['personal_information']:
                # Iterate over the profile account insights
                for insight in data['personal_information']['instagram_profile_information.json']['structure']['profile_account_insights']:
                    # Get the user who interacted with the post
                    user = insight['title']

                    # Increment the story likes counter
                    story_likes[user] = story_likes.get(user, 0) + 1

                    # Increment the comments counter
                    comments[user] = comments.get(user, 0) + 1

# Sort the users by their total interactions
users = sorted(post_likes.items(), key=lambda x: x[1] + story_likes.get(x[0], 0) + comments.get(x[0], 0), reverse=True)

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
    for user, interactions in users[:20]:
        writer.writerow([user, post_likes.get(user, 0), story_likes.get(user, 0), comments.get(user, 0)])
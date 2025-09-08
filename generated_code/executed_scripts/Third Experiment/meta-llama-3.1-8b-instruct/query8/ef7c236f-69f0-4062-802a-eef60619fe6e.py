import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the dictionary to store the user interactions
user_interactions = {}

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON data contains the 'likes' key
            if 'likes' in data:
                # Iterate over the likes
                for likes in data['likes']:
                    # Check if the likes contain the 'liked_posts.json' key
                    if 'liked_posts.json' in likes:
                        # Load the liked posts data
                        liked_posts_data = eval(likes['liked_posts.json'])

                        # Iterate over the liked posts
                        for post in liked_posts_data['likes_media_likes']:
                            # Get the user who liked the post
                            user = post['string_list_data'][0]['value']

                            # Increment the user's interaction count
                            if user in user_interactions:
                                user_interactions[user]['post_likes'] += 1
                            else:
                                user_interactions[user] = {'post_likes': 1, 'story_likes': 0, 'comments': 0}

                    # Check if the likes contain the 'liked_comments.json' key
                    if 'liked_comments.json' in likes:
                        # Load the liked comments data
                        liked_comments_data = eval(likes['liked_comments.json'])

                        # Iterate over the liked comments
                        for comment in liked_comments_data['likes_comment_likes']:
                            # Get the user who liked the comment
                            user = comment['string_list_data'][0]['value']

                            # Increment the user's interaction count
                            if user in user_interactions:
                                user_interactions[user]['comments'] += 1
                            else:
                                user_interactions[user] = {'post_likes': 0, 'story_likes': 0, 'comments': 1}

            # Check if the JSON data contains the 'messages' key
            if 'messages' in data:
                # Iterate over the messages
                for message in data['messages']:
                    # Check if the message contains the 'inbox' key
                    if 'inbox' in message:
                        # Iterate over the inbox messages
                        for inbox_message in message['inbox']:
                            # Check if the inbox message contains the 'message_1.json' key
                            if 'message_1.json' in inbox_message:
                                # Load the message data
                                message_data = eval(inbox_message['message_1.json'])

                                # Get the user who sent the message
                                user = message_data['participants'][0]['name']

                                # Increment the user's interaction count
                                if user in user_interactions:
                                    user_interactions[user]['comments'] += 1
                                else:
                                    user_interactions[user] = {'post_likes': 0, 'story_likes': 0, 'comments': 1}

# Sort the user interactions by the total count in descending order
sorted_user_interactions = sorted(user_interactions.items(), key=lambda x: x[1]['post_likes'] + x[1]['story_likes'] + x[1]['comments'], reverse=True)

# Write the sorted user interactions to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for user, interactions in sorted_user_interactions[:20]:
        writer.writerow({'User': user, 'Post Likes': interactions['post_likes'], 'Story Likes': 0, 'Comments': interactions['comments']})
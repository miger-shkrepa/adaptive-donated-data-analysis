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

            # Check if the JSON data contains the required structure
            if 'likes' in data and 'liked_comments.json' in data['likes']:
                # Load the liked comments data
                liked_comments = data['likes']['liked_comments.json']

                # Iterate over the liked comments
                for comment in liked_comments['structure']['likes_comment_likes']:
                    # Get the user who liked the comment
                    user = comment['string_list_data'][0]['href']

                    # Increment the user's interaction count
                    if user in user_interactions:
                        user_interactions[user]['post_likes'] += 1
                        user_interactions[user]['story_likes'] += 1
                        user_interactions[user]['comments'] += 1
                    else:
                        user_interactions[user] = {
                            'post_likes': 1,
                            'story_likes': 1,
                            'comments': 1
                        }

            # Check if the JSON data contains the required structure
            elif 'story_interactions' in data:
                # Iterate over the story interactions
                for interaction in data['story_interactions'].values():
                    # Check if the interaction is a JSON file
                    if interaction['type'] == 'json':
                        # Load the interaction data
                        interaction_data = interaction['structure']

                        # Iterate over the interaction data
                        for item in interaction_data.values():
                            # Check if the item is a list
                            if isinstance(item, list):
                                # Iterate over the items in the list
                                for item_data in item:
                                    # Get the user who interacted with the item
                                    user = item_data['href']

                                    # Increment the user's interaction count
                                    if user in user_interactions:
                                        user_interactions[user]['post_likes'] += 1
                                        user_interactions[user]['story_likes'] += 1
                                        user_interactions[user]['comments'] += 1
                                    else:
                                        user_interactions[user] = {
                                            'post_likes': 1,
                                            'story_likes': 1,
                                            'comments': 1
                                        }

# Sort the user interactions by the total number of interactions
sorted_interactions = sorted(user_interactions.items(), key=lambda x: x[1]['post_likes'] + x[1]['story_likes'] + x[1]['comments'], reverse=True)

# Write the sorted interactions to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
    for user, interactions in sorted_interactions[:20]:
        writer.writerow([user, interactions['post_likes'], interactions['story_likes'], interactions['comments']])
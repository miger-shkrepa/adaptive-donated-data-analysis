import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the output CSV file
output_file = 'query_responses/results.csv'

# Initialize the CSV writer
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])

    # Initialize the dictionary to store the user interactions
    user_interactions = {}

    # Iterate over the directory structure
    for dir, subdirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.json'):
                # Open the JSON file
                with open(os.path.join(dir, file), 'r') as json_file:
                    data = json.load(json_file)

                    # Check if the file contains the required data
                    if 'likes' in data and 'media_likes' in data['likes']:
                        # Extract the user interactions from the file
                        for interaction in data['likes']['media_likes']:
                            user = interaction['title']
                            post_likes = 0
                            story_likes = 0
                            comments = 0

                            # Check if the interaction contains the required data
                            if 'string_list_data' in interaction and 'timestamp' in interaction['string_list_data'][0]:
                                post_likes = len(interaction['string_list_data'])

                            # Check if the interaction contains the required data
                            if 'string_list_data' in interaction and 'timestamp' in interaction['string_list_data'][0]:
                                story_likes = len(interaction['string_list_data'])

                            # Check if the interaction contains the required data
                            if 'string_map_data' in interaction and 'value' in interaction['string_map_data']:
                                comments = len(interaction['string_map_data'])

                            # Update the user interactions dictionary
                            if user in user_interactions:
                                user_interactions[user]['Post Likes'] += post_likes
                                user_interactions[user]['Story Likes'] += story_likes
                                user_interactions[user]['Comments'] += comments
                            else:
                                user_interactions[user] = {
                                    'Post Likes': post_likes,
                                    'Story Likes': story_likes,
                                    'Comments': comments
                                }

    # Sort the user interactions by the total number of interactions
    sorted_interactions = sorted(user_interactions.items(), key=lambda x: sum(x[1].values()), reverse=True)

    # Write the top 20 user interactions to the output CSV file
    with open(output_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for user, interactions in sorted_interactions[:20]:
            writer.writerow([user, interactions['Post Likes'], interactions['Story Likes'], interactions['Comments']])
import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the data structures to store the results
user_interactions = {}

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
                # Extract the user interactions from the JSON data
                for interaction in data['likes']['liked_posts.json']['structure']['likes_media_likes']:
                    # Extract the user and the interaction type
                    user = interaction['title']
                    interaction_type = 'Post Likes'

                    # Update the user interactions dictionary
                    if user not in user_interactions:
                        user_interactions[user] = {'Post Likes': 0, 'Story Likes': 0, 'Comments': 0}

                    # Increment the interaction count
                    user_interactions[user][interaction_type] += 1

            elif 'personal_information' in data and 'personal_information.json' in data['personal_information']:
                # Extract the user interactions from the JSON data
                for interaction in data['personal_information']['personal_information.json']['structure']['profile_user']:
                    # Extract the user and the interaction type
                    user = interaction['media_map_data']['Profile Photo']['title']
                    interaction_type = 'Comments'

                    # Update the user interactions dictionary
                    if user not in user_interactions:
                        user_interactions[user] = {'Post Likes': 0, 'Story Likes': 0, 'Comments': 0}

                    # Increment the interaction count
                    user_interactions[user][interaction_type] += 1

            elif 'events' in data and 'event_reminders.json' in data['events']:
                # Extract the user interactions from the JSON data
                for interaction in data['events']['event_reminders.json']['structure']['events_event_reminders']:
                    # Extract the user and the interaction type
                    user = interaction['title']
                    interaction_type = 'Comments'

                    # Update the user interactions dictionary
                    if user not in user_interactions:
                        user_interactions[user] = {'Post Likes': 0, 'Story Likes': 0, 'Comments': 0}

                    # Increment the interaction count
                    user_interactions[user][interaction_type] += 1

# Sort the user interactions by the total number of interactions in descending order
sorted_interactions = sorted(user_interactions.items(), key=lambda x: sum(x[1].values()), reverse=True)

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
    for user, interactions in sorted_interactions[:20]:
        writer.writerow([user, interactions['Post Likes'], interactions['Story Likes'], interactions['Comments']])
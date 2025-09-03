import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the user interactions
user_interactions = {}

# Iterate over the media directory
for year in os.listdir(os.path.join(root_dir, "media")):
    for month in os.listdir(os.path.join(root_dir, "media", year)):
        for file in os.listdir(os.path.join(root_dir, "media", year, month)):
            # Check if the file is a JSON file
            if file.endswith(".json"):
                # Open the JSON file
                with open(os.path.join(root_dir, "media", year, month, file), "r") as f:
                    # Load the JSON data
                    data = json.load(f)
                    # Check if the JSON data contains the required information
                    if "profile_user" in data["structure"]:
                        # Iterate over the user interactions
                        for interaction in data["structure"]["profile_user"]:
                            # Get the user ID
                            user_id = interaction["media_map_data"]["Profile Photo"]["uri"]
                            # Get the post likes, story likes, and comments
                            post_likes = 0
                            story_likes = 0
                            comments = 0
                            # Check if the interaction contains the required information
                            if "creation_timestamp" in interaction["media_map_data"]["Profile Photo"]:
                                post_likes = 1
                            if "cross_post_source" in interaction["media_map_data"]["Profile Photo"]:
                                story_likes = 1
                            if "media_metadata" in interaction["media_map_data"]["Profile Photo"]:
                                comments = 1
                            # Update the user interactions
                            if user_id in user_interactions:
                                user_interactions[user_id]["post_likes"] += post_likes
                                user_interactions[user_id]["story_likes"] += story_likes
                                user_interactions[user_id]["comments"] += comments
                            else:
                                user_interactions[user_id] = {
                                    "post_likes": post_likes,
                                    "story_likes": story_likes,
                                    "comments": comments
                                }

# Sort the user interactions by the total interactions
user_interactions = dict(sorted(user_interactions.items(), key=lambda item: item[1]["post_likes"] + item[1]["story_likes"] + item[1]["comments"], reverse=True))

# Initialize a list to store the top 20 users
top_users = []
# Iterate over the user interactions
for user, interactions in user_interactions.items():
    # Add the user to the top users list
    top_users.append([user, interactions["post_likes"], interactions["story_likes"], interactions["comments"]])
    # Check if the top users list has reached 20 users
    if len(top_users) == 20:
        break

# Write the top users to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    # Write the top users
    for user in top_users:
        writer.writerow(user)
import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the user interactions
user_interactions = {}

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the file contains user interactions
            if "likes" in data and "media" in data["likes"]:
                # Iterate over the user interactions
                for user in data["likes"]["media"]:
                    # Check if the user is already in the dictionary
                    if user in user_interactions:
                        # Increment the user's interaction count
                        user_interactions[user]["post_likes"] += 1
                        user_interactions[user]["story_likes"] += 1
                        user_interactions[user]["comments"] += 1
                    else:
                        # Add the user to the dictionary with an interaction count of 1
                        user_interactions[user] = {"post_likes": 1, "story_likes": 1, "comments": 1}

            # Check if the file contains message requests
            elif "message_requests" in data:
                # Iterate over the message requests
                for user in data["message_requests"]:
                    # Check if the user is already in the dictionary
                    if user in user_interactions:
                        # Increment the user's interaction count
                        user_interactions[user]["comments"] += 1
                    else:
                        # Add the user to the dictionary with an interaction count of 1
                        user_interactions[user] = {"post_likes": 0, "story_likes": 0, "comments": 1}

# Sort the user interactions by the total interaction count in descending order
sorted_users = sorted(user_interactions.items(), key=lambda x: x[1]["post_likes"] + x[1]["story_likes"] + x[1]["comments"], reverse=True)

# Initialize a list to store the top 20 users
top_users = []

# Iterate over the sorted users
for user, interactions in sorted_users:
    # Add the user to the list of top users
    top_users.append([user, interactions["post_likes"], interactions["story_likes"], interactions["comments"]])

    # Check if we have reached the top 20 users
    if len(top_users) == 20:
        break

# Write the top users to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    writer.writerows(top_users)
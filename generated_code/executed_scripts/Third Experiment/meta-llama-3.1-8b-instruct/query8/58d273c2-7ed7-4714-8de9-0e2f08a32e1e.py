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

            # Check if the JSON file contains the required data
            if "story_activities_questions" in data["story_interactions"]:
                # Iterate over the story activities
                for story_activity in data["story_interactions"]["story_activities_questions"]:
                    # Check if the story activity contains the required data
                    if "string_list_data" in story_activity:
                        # Iterate over the string list data
                        for string_data in story_activity["string_list_data"]:
                            # Check if the string data contains the required data
                            if "href" in string_data and "timestamp" in string_data and "value" in string_data:
                                # Extract the user ID, post likes, story likes, and comments
                                user_id = string_data["href"]
                                post_likes = 0
                                story_likes = 0
                                comments = 0

                                # Check if the user ID is already in the dictionary
                                if user_id in user_interactions:
                                    # Update the user interactions
                                    user_interactions[user_id]["post_likes"] += post_likes
                                    user_interactions[user_id]["story_likes"] += story_likes
                                    user_interactions[user_id]["comments"] += comments
                                else:
                                    # Add the user to the dictionary
                                    user_interactions[user_id] = {
                                        "post_likes": post_likes,
                                        "story_likes": story_likes,
                                        "comments": comments
                                    }

            # Check if the JSON file contains the required data
            if "saved_saved_media" in data["media"]["saved_posts"]:
                # Iterate over the saved media
                for saved_media in data["media"]["saved_posts"]["saved_saved_media"]:
                    # Check if the saved media contains the required data
                    if "string_map_data" in saved_media:
                        # Extract the user ID and comments
                        user_id = saved_media["title"]
                        comments = 0

                        # Check if the user ID is already in the dictionary
                        if user_id in user_interactions:
                            # Update the user interactions
                            user_interactions[user_id]["comments"] += comments
                        else:
                            # Add the user to the dictionary
                            user_interactions[user_id] = {
                                "post_likes": 0,
                                "story_likes": 0,
                                "comments": comments
                            }

# Sort the user interactions by the total interactions in descending order
sorted_user_interactions = sorted(user_interactions.items(), key=lambda x: x[1]["post_likes"] + x[1]["story_likes"] + x[1]["comments"], reverse=True)

# Write the sorted user interactions to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for user_id, interactions in sorted_user_interactions[:20]:
        writer.writerow([user_id, interactions["post_likes"], interactions["story_likes"], interactions["comments"]])
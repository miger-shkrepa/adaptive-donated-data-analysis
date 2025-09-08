import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

try:
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
except FileNotFoundError as e:
    print(e)
    exit()

# Initialize variables to store engagement data
engagement_data = {}

# Iterate through the 'your_instagram_activity' directory
for item in os.listdir(root_dir):
    if item == "your_instagram_activity":
        # Iterate through the 'likes' and 'saved' directories
        for sub_item in os.listdir(os.path.join(root_dir, item)):
            if sub_item == "likes":
                # Load the 'liked_posts.json' file
                with open(os.path.join(root_dir, item, sub_item, "liked_posts.json"), "r") as f:
                    liked_posts = json.load(f)
                # Check if the 'structure' key exists in the 'liked_posts' dictionary
                if "structure" in liked_posts:
                    # Extract the 'likes_media_likes' data
                    likes_media_likes = liked_posts["structure"]["likes_media_likes"]
                    # Iterate through the 'likes_media_likes' data
                    for post in likes_media_likes:
                        # Extract the 'string_list_data' and 'title' data
                        string_list_data = post.get("string_list_data", [])
                        title = post.get("title", "")
                        # Iterate through the 'string_list_data' data
                        for item in string_list_data:
                            # Extract the 'href' and 'value' data
                            href = item.get("href", "")
                            value = item.get("value", "")
                            # Increment the engagement count for the user
                            if href in engagement_data:
                                engagement_data[href]["count"] += 1
                            else:
                                engagement_data[href] = {"title": title, "count": 1}
            elif sub_item == "saved":
                # Load the 'saved_posts.json' file
                with open(os.path.join(root_dir, item, sub_item, "saved_posts.json"), "r") as f:
                    saved_posts = json.load(f)
                # Check if the 'structure' key exists in the 'saved_posts' dictionary
                if "structure" in saved_posts:
                    # Extract the 'saved_saved_media' data
                    saved_saved_media = saved_posts["structure"]["saved_saved_media"]
                    # Iterate through the 'saved_saved_media' data
                    for post in saved_saved_media:
                        # Extract the 'string_map_data' and 'title' data
                        string_map_data = post.get("string_map_data", {})
                        title = post.get("title", "")
                        # Extract the 'Saved on' data
                        saved_on = string_map_data.get("Saved on", {})
                        # Extract the 'href' and 'timestamp' data
                        href = saved_on.get("href", "")
                        timestamp = saved_on.get("timestamp", 0)
                        # Increment the engagement count for the user
                        if href in engagement_data:
                            engagement_data[href]["count"] += 1
                        else:
                            engagement_data[href] = {"title": title, "count": 1}

# Create a list to store the engagement data
engagement_list = []
# Iterate through the engagement data
for user, data in engagement_data.items():
    # Append the user and engagement count to the list
    engagement_list.append([data["title"], data["count"]])

# Write the engagement data to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    # Write the column headers
    writer.writerow(["User", "Times Engaged"])
    # Write the engagement data
    writer.writerows(engagement_list)
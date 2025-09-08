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

# Initialize an empty list to store the profiles that do not follow back
profiles_not_following_back = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as f:
            # Load the JSON data
            data = json.load(f)
            # Check if the JSON data has the expected structure
            if "likes" in data and "liked_posts.json" in data["likes"] and "structure" in data["likes"]["liked_posts.json"]:
                # Extract the liked posts data
                liked_posts_data = data["likes"]["liked_posts.json"]["structure"]["likes_media_likes"]
                # Iterate over the liked posts
                for post in liked_posts_data:
                    # Check if the post has the expected structure
                    if "string_list_data" in post and "href" in post["string_list_data"][0] and "timestamp" in post["string_list_data"][0] and "value" in post["string_list_data"][0]:
                        # Extract the post data
                        post_data = post["string_list_data"][0]
                        # Check if the post data has the expected structure
                        if "href" in post_data and "timestamp" in post_data and "value" in post_data:
                            # Extract the post href and timestamp
                            post_href = post_data["href"]
                            post_timestamp = post_data["timestamp"]
                            # Check if the post href is in the saved posts data
                            if "saved" in data and "saved_posts.json" in data["saved"] and "structure" in data["saved"]["saved_posts.json"]:
                                # Extract the saved posts data
                                saved_posts_data = data["saved"]["saved_posts.json"]["structure"]["saved_saved_media"]
                                # Iterate over the saved posts
                                for saved_post in saved_posts_data:
                                    # Check if the saved post has the expected structure
                                    if "string_map_data" in saved_post and "Saved on" in saved_post["string_map_data"] and "href" in saved_post["string_map_data"]["Saved on"] and "timestamp" in saved_post["string_map_data"]["Saved on"]:
                                        # Extract the saved post data
                                        saved_post_data = saved_post["string_map_data"]["Saved on"]
                                        # Check if the saved post data has the expected structure
                                        if "href" in saved_post_data and "timestamp" in saved_post_data:
                                            # Extract the saved post href and timestamp
                                            saved_post_href = saved_post_data["href"]
                                            saved_post_timestamp = saved_post_data["timestamp"]
                                            # Check if the post href is not the same as the saved post href and the post timestamp is less than the saved post timestamp
                                            if post_href != saved_post_href and post_timestamp < saved_post_timestamp:
                                                # Add the post href to the list of profiles that do not follow back
                                                profiles_not_following_back.append(post_href)

# Write the list of profiles that do not follow back to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Profile"])  # Write the column headers
    for profile in profiles_not_following_back:
        writer.writerow([profile])  # Write each profile to a new row
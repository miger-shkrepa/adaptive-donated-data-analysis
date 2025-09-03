import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the results
results = []

# Define the path to the logged_information directory
logged_info_dir = os.path.join(root_dir, "logged_information")

# Check if the logged_information directory exists
if not os.path.exists(logged_info_dir):
    # If it doesn't exist, add a row with column headers and save the CSV file
    results.append(["Account", "Post Views", "Video Views"])
else:
    # Define the path to the posts_and_stories_view_info.json file
    posts_and_stories_view_info_file = os.path.join(logged_info_dir, "posts_and_stories_view_info.json")

    # Check if the posts_and_stories_view_info.json file exists
    if not os.path.exists(posts_and_stories_view_info_file):
        # If it doesn't exist, add a row with column headers and save the CSV file
        results.append(["Account", "Post Views", "Video Views"])
    else:
        # Load the JSON data from the posts_and_stories_view_info.json file
        with open(posts_and_stories_view_info_file, "r") as f:
            data = json.load(f)

        # Iterate over the data and extract the required information
        for item in data:
            account = item["string_map_data"]["Account"]["value"]
            post_views = item["string_map_data"]["Post Views"]["value"]
            video_views = item["string_map_data"]["Video Views"]["value"]

            # Append the results to the list
            results.append([account, post_views, video_views])

# Save the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(results)
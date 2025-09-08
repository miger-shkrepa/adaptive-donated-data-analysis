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

# Define the path to the ads_viewed.json file
ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")

# Check if the ads_viewed.json file exists
if os.path.exists(ads_viewed_path):
    # Open the ads_viewed.json file
    with open(ads_viewed_path, "r") as f:
        # Load the JSON data
        data = json.load(f)

        # Iterate over the impressions_history_ads_seen list
        for item in data["impressions_history_ads_seen"]:
            # Get the author of the ad
            author = item["string_map_data"].get("Author", {}).get("value", "")

            # If the author is not empty, add it to the results list
            if author:
                results.append([author, 1, 0])

# Define the path to the videos_watched.json file
videos_watched_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")

# Check if the videos_watched.json file exists
if os.path.exists(videos_watched_path):
    # Open the videos_watched.json file
    with open(videos_watched_path, "r") as f:
        # Load the JSON data
        data = json.load(f)

        # Iterate over the impressions_history_videos_watched list
        for item in data["impressions_history_videos_watched"]:
            # Get the author of the video
            author = item["string_map_data"].get("Author", {}).get("value", "")

            # If the author is not empty, add it to the results list
            if author:
                # Check if the author is already in the results list
                author_found = False
                for result in results:
                    if result[0] == author:
                        # If the author is already in the results list, increment the video views
                        result[2] += 1
                        author_found = True
                        break

                # If the author is not in the results list, add it to the results list
                if not author_found:
                    results.append([author, 0, 1])

# Define the path to the posts_viewed.json file
posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")

# Check if the posts_viewed.json file exists
if os.path.exists(posts_viewed_path):
    # Open the posts_viewed.json file
    with open(posts_viewed_path, "r") as f:
        # Load the JSON data
        data = json.load(f)

        # Iterate over the impressions_history_posts_seen list
        for item in data["impressions_history_posts_seen"]:
            # Get the author of the post
            author = item["string_map_data"].get("Author", {}).get("value", "")

            # If the author is not empty, add it to the results list
            if author:
                # Check if the author is already in the results list
                author_found = False
                for result in results:
                    if result[0] == author:
                        # If the author is already in the results list, increment the post views
                        result[1] += 1
                        author_found = True
                        break

                # If the author is not in the results list, add it to the results list
                if not author_found:
                    results.append([author, 1, 0])

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    # Create a CSV writer
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["Account", "Post Views", "Video Views"])

    # Write the results
    writer.writerows(results)
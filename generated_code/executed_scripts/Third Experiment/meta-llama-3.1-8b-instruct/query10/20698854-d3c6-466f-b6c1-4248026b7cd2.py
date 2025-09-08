import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the counters
post_views = 0
video_views = 0
accounts = set()

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON file contains the required data
            if "ads_viewed.json" in filename:
                # Iterate over the impressions history ads seen
                for impression in data["structure"]["impressions_history_ads_seen"]:
                    # Increment the post views counter
                    post_views += 1
                    # Add the account to the set of accounts
                    accounts.add("ads_viewed")

            elif "posts_viewed.json" in filename:
                # Iterate over the impressions history posts seen
                for impression in data["structure"]["impressions_history_posts_seen"]:
                    # Increment the post views counter
                    post_views += 1
                    # Add the account to the set of accounts
                    accounts.add("posts_viewed")

            elif "videos_watched.json" in filename:
                # Iterate over the impressions history videos watched
                for impression in data["structure"]["impressions_history_videos_watched"]:
                    # Increment the video views counter
                    video_views += 1
                    # Add the account to the set of accounts
                    accounts.add("videos_watched")

# Create the CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(["Account", "Post Views", "Video Views"])
    # Write the data
    for account in accounts:
        writer.writerow([account, post_views if account == "ads_viewed" or account == "posts_viewed" else 0, video_views if account == "videos_watched" else 0])
import csv
import json
import os

# Define the root directory variable
root_dir = "root_dir"

try:
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
except FileNotFoundError as e:
    print(e)
    exit()

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Account', 'Post Views', 'Video Views']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the column headers
    writer.writeheader()

    # Initialize the counters
    post_views = 0
    video_views = 0

    # Iterate over the subdirectories
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Check if the 'your_instagram_activity' directory exists
        if 'your_instagram_activity' not in dirnames:
            continue

        # Iterate over the files in the 'your_instagram_activity' directory
        for filename in filenames:
            # Check if the file is a JSON file
            if filename.endswith('.json'):
                # Open the JSON file
                with open(os.path.join(dirpath, filename), 'r') as json_file:
                    # Load the JSON data
                    data = json.load(json_file)

                    # Check if the file contains the required data
                    if 'likes' in data and 'liked_posts.json' in data['likes']:
                        # Extract the post views
                        post_views += len(data['likes']['liked_posts.json']['structure']['likes_media_likes'])

                    elif 'saved' in data and 'saved_posts.json' in data['saved']:
                        # Extract the post views
                        post_views += len(data['saved']['saved_posts.json']['structure']['saved_saved_media'])

                    elif 'likes' in data and 'liked_posts.json' in data['likes']:
                        # Extract the video views
                        video_views += len(data['likes']['liked_posts.json']['structure']['likes_media_likes'])

                    elif 'saved' in data and 'saved_posts.json' in data['saved']:
                        # Extract the video views
                        video_views += len(data['saved']['saved_posts.json']['structure']['saved_saved_media'])

    # Write the results to the CSV file
    writer.writerow({'Account': 'Total', 'Post Views': post_views, 'Video Views': video_views})
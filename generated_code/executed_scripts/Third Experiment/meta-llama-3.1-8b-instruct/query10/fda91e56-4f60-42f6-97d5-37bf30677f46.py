import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Account', 'Post Views', 'Video Views']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Initialize the counters
    post_views = 0
    video_views = 0

    # Iterate over the files in the root directory
    for filename in os.listdir(root_dir):
        # Check if the file is a JSON file
        if filename.endswith('.json'):
            # Open the file
            with open(os.path.join(root_dir, filename), 'r') as file:
                # Load the JSON data
                data = json.load(file)

                # Check if the file contains post views data
                if 'impressions_history_posts_seen' in data['structure']:
                    # Increment the post views counter
                    post_views += len(data['structure']['impressions_history_posts_seen'])

                # Check if the file contains video views data
                if 'impressions_history_videos_watched' in data['structure']:
                    # Increment the video views counter
                    video_views += len(data['structure']['impressions_history_videos_watched'])

    # Write the results to the CSV file
    writer.writerow({'Account': 'Total', 'Post Views': post_views, 'Video Views': video_views})
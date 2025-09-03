import csv
import os

# Declare the file input variable
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Account', 'Post Views', 'Video Views']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the column headers
    writer.writeheader()

    # Initialize the counters
    post_views = 0
    video_views = 0

    # Iterate over the JSON files in the root directory
    for filename in os.listdir(root_dir):
        if filename.endswith('.json'):
            # Open the JSON file
            with open(os.path.join(root_dir, filename), 'r') as json_file:
                data = json.load(json_file)

                # Check if the JSON file contains the required data
                if 'events' in data and 'likes' in data['events']:
                    # Iterate over the likes in the JSON file
                    for like in data['events']['likes']['liked_comments.json']['likes_comment_likes']:
                        # Check if the like is a post or a video
                        if 'string_list_data' in like and len(like['string_list_data']) > 0:
                            # Increment the post views counter
                            post_views += 1
                        elif 'exif_data' in like and len(like['exif_data']) > 0:
                            # Increment the video views counter
                            video_views += 1

                # Write the data to the CSV file
                writer.writerow({'Account': filename, 'Post Views': post_views, 'Video Views': video_views})

                # Reset the counters
                post_views = 0
                video_views = 0
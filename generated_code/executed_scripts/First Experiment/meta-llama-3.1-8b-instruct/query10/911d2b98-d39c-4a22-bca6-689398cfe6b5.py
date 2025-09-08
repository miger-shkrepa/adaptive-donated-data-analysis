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

    # Iterate over the JSON files in the root directory
    for filename in os.listdir(root_dir):
        if filename.endswith('.json'):
            # Open the JSON file
            with open(os.path.join(root_dir, filename), 'r') as json_file:
                data = json.load(json_file)

                # Check if the JSON file contains the required data
                if 'ads_and_topics' in data and 'ads_viewed.json' in data['ads_and_topics']:
                    # Extract the post views and video views
                    post_views = 0
                    video_views = 0
                    for impression in data['ads_and_topics']['ads_viewed.json']['structure']['impressions_history_ads_seen']:
                        post_views += 1
                        if 'string_map_data' in impression and 'Time' in impression['string_map_data'] and impression['string_map_data']['Time']['timestamp'] > 0:
                            video_views += 1

                    # Write the data to the CSV file
                    writer.writerow({'Account': filename[:-5], 'Post Views': post_views, 'Video Views': video_views})

                elif 'ads_and_topics' in data and 'posts_viewed.json' in data['ads_and_topics']:
                    # Extract the post views and video views
                    post_views = 0
                    video_views = 0
                    for impression in data['ads_and_topics']['posts_viewed.json']['structure']['impressions_history_posts_seen']:
                        post_views += 1
                        if 'string_map_data' in impression and 'Time' in impression['string_map_data'] and impression['string_map_data']['Time']['timestamp'] > 0:
                            video_views += 1

                    # Write the data to the CSV file
                    writer.writerow({'Account': filename[:-5], 'Post Views': post_views, 'Video Views': video_views})

                elif 'ads_and_topics' in data and 'videos_watched.json' in data['ads_and_topics']:
                    # Extract the post views and video views
                    post_views = 0
                    video_views = 0
                    for impression in data['ads_and_topics']['videos_watched.json']['structure']['impressions_history_videos_watched']:
                        video_views += 1
                        if 'string_map_data' in impression and 'Time' in impression['string_map_data'] and impression['string_map_data']['Time']['timestamp'] > 0:
                            post_views += 1

                    # Write the data to the CSV file
                    writer.writerow({'Account': filename[:-5], 'Post Views': post_views, 'Video Views': video_views})

                else:
                    raise ValueError("ValueError: The JSON file does not contain the required data.")
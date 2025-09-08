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
                # Load the JSON data
                data = json.load(json_file)

                # Iterate over the data
                for item in data['ads_information']['ads_and_topics'].values():
                    # Check if the item has a 'structure' key
                    if 'structure' in item:
                        # Iterate over the structure
                        for key, value in item['structure'].items():
                            # Check if the key is 'impressions_history_ads_seen' or 'impressions_history_videos_watched'
                            if key in ['impressions_history_ads_seen', 'impressions_history_videos_watched']:
                                # Get the account name from the key
                                account = key.replace('impressions_history_', '').replace('_seen', '').replace('_watched', '')

                                # Initialize the post views and video views counters
                                post_views = 0
                                video_views = 0

                                # Iterate over the items in the value
                                for item in value:
                                    # Check if the item has a 'string_map_data' key
                                    if 'string_map_data' in item:
                                        # Iterate over the string map data
                                        for key, value in item['string_map_data'].items():
                                            # Check if the key is 'Author' or 'Time'
                                            if key in ['Author', 'Time']:
                                                # Increment the post views or video views counter
                                                if key == 'Author':
                                                    post_views += 1
                                                else:
                                                    video_views += 1

                                # Write the data to the CSV file
                                writer.writerow({'Account': account, 'Post Views': post_views, 'Video Views': video_views})
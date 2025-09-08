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
        for filename in filenames:
            # Check if the file is a JSON file
            if filename.endswith('.json'):
                # Open the JSON file
                with open(os.path.join(dirpath, filename), 'r') as json_file:
                    data = json.load(json_file)

                    # Check if the JSON file has the expected structure
                    if 'likes' in data and 'liked_posts.json' in data['likes']:
                        # Extract the likes data
                        likes_data = data['likes']['liked_posts.json']['structure']['likes_media_likes']

                        # Iterate over the likes data
                        for like in likes_data:
                            # Check if the like has a 'string_list_data' key
                            if 'string_list_data' in like:
                                # Extract the string list data
                                string_list_data = like['string_list_data']

                                # Iterate over the string list data
                                for string_list in string_list_data:
                                    # Check if the string list has a 'href' key
                                    if 'href' in string_list:
                                        # Extract the href value
                                        href = string_list['href']

                                        # Increment the post views counter
                                        post_views += 1

                    elif 'saved' in data and 'saved_posts.json' in data['saved']:
                        # Extract the saved data
                        saved_data = data['saved']['saved_posts.json']['structure']['saved_saved_media']

                        # Iterate over the saved data
                        for saved in saved_data:
                            # Check if the saved has a 'string_map_data' key
                            if 'string_map_data' in saved:
                                # Extract the string map data
                                string_map_data = saved['string_map_data']

                                # Check if the string map data has a 'Saved on' key
                                if 'Saved on' in string_map_data:
                                    # Extract the Saved on value
                                    saved_on = string_map_data['Saved on']

                                    # Check if the Saved on value has a 'href' key
                                    if 'href' in saved_on:
                                        # Extract the href value
                                        href = saved_on['href']

                                        # Increment the video views counter
                                        video_views += 1

    # Write the results to the CSV file
    writer.writerow({'Account': 'Total', 'Post Views': post_views, 'Video Views': video_views})
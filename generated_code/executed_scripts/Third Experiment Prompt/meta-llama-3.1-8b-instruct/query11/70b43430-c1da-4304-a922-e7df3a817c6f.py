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

# Initialize the output CSV file
output_csv = "query_responses/results.csv"

# Initialize the output CSV writer
with open(output_csv, 'w', newline='') as csvfile:
    fieldnames = ['Account']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate over the 'your_instagram_activity' directory
    for account in os.listdir(root_dir + '/your_instagram_activity'):
        if account == 'likes':
            # Iterate over the 'liked_posts.json' file
            for file in os.listdir(root_dir + '/your_instagram_activity/likes'):
                if file == 'liked_posts.json':
                    try:
                        # Load the 'liked_posts.json' file
                        with open(root_dir + '/your_instagram_activity/likes/' + file, 'r') as json_file:
                            liked_posts = json.load(json_file)
                            # Check if the 'liked_posts.json' file has a 'structure' key
                            if 'structure' in liked_posts:
                                # Iterate over the 'likes_media_likes' list
                                for post in liked_posts['structure']['likes_media_likes']:
                                    # Check if the post has a 'title' and a 'string_list_data' list
                                    if 'title' in post and 'string_list_data' in post:
                                        # Iterate over the 'string_list_data' list
                                        for data in post['string_list_data']:
                                            # Check if the data has a 'href' and a 'value'
                                            if 'href' in data and 'value' in data:
                                                # Check if the 'value' is not 'liked'
                                                if data['value'] != 'liked':
                                                    # Write the account to the output CSV file
                                                    writer.writerow({'Account': account})
                    except FileNotFoundError:
                        # If the 'liked_posts.json' file does not exist, treat its contribution as 0
                        pass
        elif account == 'saved':
            # Iterate over the 'saved_posts.json' file
            for file in os.listdir(root_dir + '/your_instagram_activity/saved'):
                if file == 'saved_posts.json':
                    try:
                        # Load the 'saved_posts.json' file
                        with open(root_dir + '/your_instagram_activity/saved/' + file, 'r') as json_file:
                            saved_posts = json.load(json_file)
                            # Check if the 'saved_posts.json' file has a 'structure' key
                            if 'structure' in saved_posts:
                                # Iterate over the 'saved_saved_media' list
                                for post in saved_posts['structure']['saved_saved_media']:
                                    # Check if the post has a 'title' and a 'string_map_data' dictionary
                                    if 'title' in post and 'string_map_data' in post:
                                        # Check if the 'string_map_data' dictionary has a 'Saved on' key
                                        if 'Saved on' in post['string_map_data']:
                                            # Check if the 'Saved on' value has a 'href' and a 'timestamp'
                                            if 'href' in post['string_map_data']['Saved on'] and 'timestamp' in post['string_map_data']['Saved on']:
                                                # Write the account to the output CSV file
                                                writer.writerow({'Account': account})
                    except FileNotFoundError:
                        # If the 'saved_posts.json' file does not exist, treat its contribution as 0
                        pass
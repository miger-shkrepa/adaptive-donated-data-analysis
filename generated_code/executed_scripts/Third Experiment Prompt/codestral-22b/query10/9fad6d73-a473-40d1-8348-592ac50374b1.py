import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

results = []

# Function to safely load JSON data
def load_json(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# Function to safely get the value from a dictionary
def get_value(dictionary, keys):
    for key in keys:
        try:
            dictionary = dictionary[key]
        except KeyError:
            return 0
    return dictionary

# Process posts_viewed.json
posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
posts_viewed_data = load_json(posts_viewed_path)
if posts_viewed_data:
    for post in posts_viewed_data['impressions_history_posts_seen']:
        account = get_value(post, ['string_map_data', 'Author', 'value'])
        if account:
            results.append([account, 1, 0])

# Process videos_watched.json
videos_watched_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'videos_watched.json')
videos_watched_data = load_json(videos_watched_path)
if videos_watched_data:
    for video in videos_watched_data['impressions_history_videos_watched']:
        account = get_value(video, ['string_map_data', 'Author', 'value'])
        if account:
            # Check if account already exists in results
            account_exists = False
            for result in results:
                if result[0] == account:
                    result[2] += 1
                    account_exists = True
                    break
            if not account_exists:
                results.append([account, 0, 1])

# Write results to CSV
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Account', 'Post Views', 'Video Views'])
    writer.writerows(results)
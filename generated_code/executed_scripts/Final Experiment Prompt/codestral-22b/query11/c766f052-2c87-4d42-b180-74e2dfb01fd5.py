import json
import csv
import os

# Declare the root directory
root_dir = "root_dir"

# Initialize empty sets to store the accounts
viewed_accounts = set()
liked_accounts = set()

# Process the posts_viewed.json file
try:
    with open(os.path.join(root_dir, 'ads_information/ads_and_topics/posts_viewed.json')) as f:
        data = json.load(f)
        for post in data.get('impressions_history_posts_seen', []):
            viewed_accounts.add(post['string_map_data']['Author']['value'])
except FileNotFoundError:
    raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")
except json.JSONDecodeError:
    raise ValueError("ValueError: The posts_viewed.json file is not a valid JSON file.")

# Process the liked_posts.json file
try:
    with open(os.path.join(root_dir, 'your_instagram_activity/likes/liked_posts.json')) as f:
        data = json.load(f)
        for post in data.get('likes_media_likes', []):
            for item in post.get('string_list_data', []):
                liked_accounts.add(item['value'])
except FileNotFoundError:
    raise FileNotFoundError("FileNotFoundError: The liked_posts.json file does not exist.")
except json.JSONDecodeError:
    raise ValueError("ValueError: The liked_posts.json file is not a valid JSON file.")

# Find the accounts that were viewed but not liked
unliked_viewed_accounts = viewed_accounts - liked_accounts

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Account'])
    for account in unliked_viewed_accounts:
        writer.writerow([account])
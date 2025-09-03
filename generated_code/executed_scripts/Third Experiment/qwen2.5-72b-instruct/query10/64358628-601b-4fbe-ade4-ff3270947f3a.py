import os
import json
import csv

root_dir = "root_dir"

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        likes_path = os.path.join(root_dir, 'your_instagram_activity', 'likes', 'liked_posts.json')
        saved_path = os.path.join(root_dir, 'your_instagram_activity', 'saved', 'saved_posts.json')

        likes_data = {}
        saved_data = {}

        if os.path.exists(likes_path):
            with open(likes_path, 'r') as likes_file:
                likes_data = json.load(likes_file)
        else:
            print("Warning: liked_posts.json does not exist. Post Views will be 0.")

        if os.path.exists(saved_path):
            with open(saved_path, 'r') as saved_file:
                saved_data = json.load(saved_file)
        else:
            print("Warning: saved_posts.json does not exist. Video Views will be 0.")

        post_views = 0
        video_views = 0

        if 'likes_media_likes' in likes_data:
            for item in likes_data['likes_media_likes']:
                for data in item['string_list_data']:
                    post_views += 1

        if 'saved_saved_media' in saved_data:
            for item in saved_data['saved_saved_media']:
                for key, value in item['string_map_data'].items():
                    if key == 'Saved on':
                        video_views += 1

        writer.writerow({'Account': 'User', 'Post Views': post_views, 'Video Views': video_views})

except FileNotFoundError as e:
    print(e)
except Exception as e:
    print(f"Error: {str(e)}")
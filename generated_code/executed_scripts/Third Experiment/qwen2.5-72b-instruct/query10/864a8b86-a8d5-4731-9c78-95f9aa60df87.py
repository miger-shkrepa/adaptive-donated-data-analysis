import os
import json
import csv

root_dir = "root_dir"

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    # Initialize the dictionary to store the results
    results = {}

    # Check if the necessary directories and files exist
    if os.path.exists(os.path.join(root_dir, "likes", "liked_posts.json")):
        with open(os.path.join(root_dir, "likes", "liked_posts.json"), 'r') as file:
            liked_posts_data = json.load(file)
            for post in liked_posts_data.get("likes_media_likes", []):
                for string_data in post.get("string_list_data", []):
                    account = string_data.get("value", "Unknown")
                    if account not in results:
                        results[account] = {"Post Views": 0, "Video Views": 0}
                    results[account]["Post Views"] += 1

    if os.path.exists(os.path.join(root_dir, "reels.json")):
        with open(os.path.join(root_dir, "reels.json"), 'r') as file:
            reels_data = json.load(file)
            for reel in reels_data.get("ig_reels", []):
                account = reel.get("title", "Unknown")
                if account not in results:
                    results[account] = {"Post Views": 0, "Video Views": 0}
                results[account]["Video Views"] += 1

    # Write the results to a CSV file
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, views in results.items():
            writer.writerow({'Account': account, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})

except FileNotFoundError as e:
    print(e)
except json.JSONDecodeError as e:
    raise ValueError(f"Error: JSON decoding error - {e}")
except Exception as e:
    raise Exception(f"Error: An unexpected error occurred - {e}")
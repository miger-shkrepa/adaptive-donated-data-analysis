import os
import json
import csv

root_dir = "root_dir"

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    # Initialize data structures
    account_views = {}

    # Check if the necessary files exist
    media_posts_path = os.path.join(root_dir, "media", "posts")
    media_other_path = os.path.join(root_dir, "media", "other")

    if not os.path.exists(media_posts_path) and not os.path.exists(media_other_path):
        # If both directories are missing, create a CSV with only headers
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account', 'Post Views', 'Video Views'])
        print("CSV file created with only headers due to missing data.")
        exit()

    # Process media posts
    if os.path.exists(media_posts_path):
        for year_folder in os.listdir(media_posts_path):
            year_path = os.path.join(media_posts_path, year_folder)
            if os.path.isdir(year_path):
                for file_name in os.listdir(year_path):
                    if file_name.endswith('.mp4'):
                        account_views.setdefault('Unknown Account', {'Post Views': 0, 'Video Views': 0})
                        account_views['Unknown Account']['Video Views'] += 1
                    elif file_name.endswith('.jpg') or file_name.endswith('.png'):
                        account_views.setdefault('Unknown Account', {'Post Views': 0, 'Video Views': 0})
                        account_views['Unknown Account']['Post Views'] += 1

    # Process other media
    if os.path.exists(media_other_path):
        for year_folder in os.listdir(media_other_path):
            year_path = os.path.join(media_other_path, year_folder)
            if os.path.isdir(year_path):
                for file_name in os.listdir(year_path):
                    if file_name.endswith('.mp4'):
                        account_views.setdefault('Unknown Account', {'Post Views': 0, 'Video Views': 0})
                        account_views['Unknown Account']['Video Views'] += 1
                    elif file_name.endswith('.jpg') or file_name.endswith('.png'):
                        account_views.setdefault('Unknown Account', {'Post Views': 0, 'Video Views': 0})
                        account_views['Unknown Account']['Post Views'] += 1

    # Write results to CSV
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Account', 'Post Views', 'Video Views'])
        for account, views in account_views.items():
            writer.writerow([account, views['Post Views'], views['Video Views']])

except FileNotFoundError as e:
    print(e)
except Exception as e:
    print(f"Error: {e}")
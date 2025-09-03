import os
import csv

root_dir = "root_dir"

def get_account_views(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        account_views = {}

        # Check for liked posts
        liked_posts_path = os.path.join(root_dir, "likes", "liked_posts.json")
        if os.path.exists(liked_posts_path):
            with open(liked_posts_path, 'r', encoding='utf-8') as file:
                import json
                liked_posts_data = json.load(file)
                for like in liked_posts_data.get('likes_media_likes', []):
                    for data in like.get('string_list_data', []):
                        account = data.get('value')
                        if account:
                            if account not in account_views:
                                account_views[account] = {'post_views': 0, 'video_views': 0}
                            account_views[account]['post_views'] += 1

        # Check for liked comments
        liked_comments_path = os.path.join(root_dir, "likes", "liked_comments.json")
        if os.path.exists(liked_comments_path):
            with open(liked_comments_path, 'r', encoding='utf-8') as file:
                import json
                liked_comments_data = json.load(file)
                for like in liked_comments_data.get('likes_comment_likes', []):
                    for data in like.get('string_list_data', []):
                        account = data.get('value')
                        if account:
                            if account not in account_views:
                                account_views[account] = {'post_views': 0, 'video_views': 0}
                            account_views[account]['post_views'] += 1

        # Check for video metadata (assuming video views are stored here)
        video_metadata_path = os.path.join(root_dir, "video_metadata")
        if os.path.exists(video_metadata_path):
            for video_file in os.listdir(video_metadata_path):
                video_file_path = os.path.join(video_metadata_path, video_file)
                if os.path.isfile(video_file_path):
                    with open(video_file_path, 'r', encoding='utf-8') as file:
                        import json
                        video_data = json.load(file)
                        for video in video_data.get('video_metadata', []):
                            account = video.get('title')  # Assuming title is the account name
                            if account:
                                if account not in account_views:
                                    account_views[account] = {'post_views': 0, 'video_views': 0}
                                account_views[account]['video_views'] += 1

        # Prepare CSV output
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Account', 'Post Views', 'Video Views']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for account, views in account_views.items():
                writer.writerow({'Account': account, 'Post Views': views['post_views'], 'Video Views': views['video_views']})

    except Exception as e:
        print(f"Error: {str(e)}")
        # Create an empty CSV with headers if there's an error
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Account', 'Post Views', 'Video Views']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

get_account_views(root_dir)
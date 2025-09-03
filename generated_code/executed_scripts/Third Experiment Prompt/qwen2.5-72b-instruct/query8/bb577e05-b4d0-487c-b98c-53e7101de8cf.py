import os
import json
import csv
from collections import defaultdict

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def get_interactions_count(file_path, key):
    try:
        data = load_json(file_path)
        interactions = defaultdict(int)
        for item in data.get(key, []):
            for string_data in item.get('string_list_data', []):
                interactions[string_data.get('value', '')] += 1
        return interactions
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return defaultdict(int)

def get_comments_count(file_path):
    try:
        data = load_json(file_path)
        interactions = defaultdict(int)
        for item in data.get('comments_reels_comments', []):
            media_owner = item['string_map_data'].get('Media Owner', '')
            interactions[media_owner] += 1
        return interactions
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return defaultdict(int)

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        post_likes_file = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        story_likes_file = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
        comments_file = os.path.join(root_dir, "your_instagram_activity", "comments", "reels_comments.json")

        post_likes = get_interactions_count(post_likes_file, 'likes_media_likes') if os.path.exists(post_likes_file) else defaultdict(int)
        story_likes = get_interactions_count(story_likes_file, 'story_activities_story_likes') if os.path.exists(story_likes_file) else defaultdict(int)
        comments = get_comments_count(comments_file) if os.path.exists(comments_file) else defaultdict(int)

        interactions = defaultdict(int)
        for account in set(post_likes.keys()).union(story_likes.keys()).union(comments.keys()):
            interactions[account] = post_likes[account] + story_likes[account] + comments[account]

        top_accounts = sorted(interactions.items(), key=lambda x: x[1], reverse=True)[:20]

        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
            for account, count in top_accounts:
                writer.writerow([account, post_likes[account], story_likes[account], comments[account]])

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
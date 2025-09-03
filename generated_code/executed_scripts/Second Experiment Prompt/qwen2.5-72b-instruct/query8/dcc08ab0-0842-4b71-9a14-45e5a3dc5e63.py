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
        return None
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def get_interactions_count(file_path, key):
    data = load_json(file_path)
    if data is None:
        return defaultdict(int)
    
    interactions = defaultdict(int)
    try:
        for item in data[key]:
            for string_data in item['string_list_data']:
                if 'value' in string_data:
                    interactions[string_data['value']] += 1
    except KeyError:
        pass
    return interactions

def get_comments_count(file_path):
    data = load_json(file_path)
    if data is None:
        return defaultdict(int)
    
    interactions = defaultdict(int)
    try:
        for item in data['comments_reels_comments']:
            media_owner = item['string_map_data']['Media Owner']['value']
            interactions[media_owner] += 1
    except KeyError:
        pass
    return interactions

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    post_likes = get_interactions_count(
        os.path.join(root_dir, 'your_instagram_activity', 'likes', 'liked_posts.json'),
        'likes_media_likes'
    )

    story_likes = get_interactions_count(
        os.path.join(root_dir, 'your_instagram_activity', 'story_interactions', 'story_likes.json'),
        'story_activities_story_likes'
    )

    comments = get_comments_count(
        os.path.join(root_dir, 'your_instagram_activity', 'comments', 'reels_comments.json')
    )

    interactions = defaultdict(int)
    for account, count in post_likes.items():
        interactions[account] += count
    for account, count in story_likes.items():
        interactions[account] += count
    for account, count in comments.items():
        interactions[account] += count

    top_accounts = sorted(interactions.items(), key=lambda x: x[1], reverse=True)[:20]

    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, count in top_accounts:
            writer.writerow({
                'User': account,
                'Post Likes': post_likes.get(account, 0),
                'Story Likes': story_likes.get(account, 0),
                'Comments': comments.get(account, 0)
            })

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
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

def process_likes(file_path, interaction_type):
    try:
        data = load_json(file_path)
        interactions = defaultdict(int)
        for entry in data.get(interaction_type, []):
            for item in entry.get('string_list_data', []):
                interactions[item['value']] += 1
        return interactions
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return defaultdict(int)

def process_comments(file_path):
    try:
        data = load_json(file_path)
        interactions = defaultdict(int)
        for entry in data:
            interactions[entry['string_map_data']['Media Owner']] += 1
        return interactions
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return defaultdict(int)

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    post_likes = process_likes(os.path.join(root_dir, 'your_instagram_activity', 'likes', 'liked_posts.json'), 'likes_media_likes')
    story_likes = process_likes(os.path.join(root_dir, 'your_instagram_activity', 'story_interactions', 'story_likes.json'), 'story_activities_story_likes')
    comments = process_comments(os.path.join(root_dir, 'your_instagram_activity', 'comments', 'post_comments_1.json'))

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
        for account, total in top_accounts:
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
        print(f"Error: {e}")
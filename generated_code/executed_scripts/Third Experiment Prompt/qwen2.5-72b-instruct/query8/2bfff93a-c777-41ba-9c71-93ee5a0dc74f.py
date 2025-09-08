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

def get_interactions_counts(root_dir):
    interactions = defaultdict(int)
    
    try:
        # Post Likes
        post_likes_path = os.path.join(root_dir, 'your_instagram_activity', 'likes', 'liked_posts.json')
        if os.path.exists(post_likes_path):
            post_likes_data = load_json(post_likes_path)
            for post in post_likes_data.get('likes_media_likes', []):
                for item in post.get('string_list_data', []):
                    interactions[item['value']] += 1

        # Story Likes
        story_likes_path = os.path.join(root_dir, 'your_instagram_activity', 'story_interactions', 'story_likes.json')
        if os.path.exists(story_likes_path):
            story_likes_data = load_json(story_likes_path)
            for story in story_likes_data.get('story_activities_story_likes', []):
                for item in story.get('string_list_data', []):
                    if 'value' in item:
                        interactions[item['value']] += 1

        # Comments
        comments_path = os.path.join(root_dir, 'your_instagram_activity', 'comments', 'post_comments_1.json')
        if os.path.exists(comments_path):
            comments_data = load_json(comments_path)
            for comment in comments_data:
                if 'Media Owner' in comment['string_map_data']:
                    interactions[comment['string_map_data']['Media Owner']['value']] += 1

    except Exception as e:
        print(f"Error: {e}")
    
    return dict(sorted(interactions.items(), key=lambda x: x[1], reverse=True)[:20])

def write_to_csv(data, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        if not data:
            return
        
        for user, count in data.items():
            writer.writerow({
                'User': user,
                'Post Likes': count,
                'Story Likes': count,
                'Comments': count
            })

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    interactions_counts = get_interactions_counts(root_dir)
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    write_to_csv(interactions_counts, output_path)

if __name__ == "__main__":
    main()
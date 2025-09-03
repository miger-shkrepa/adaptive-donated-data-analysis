import os
import csv
from collections import defaultdict

root_dir = "root_dir"

def load_json_file(file_path):
    import json
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

def get_interactions_from_file(file_path, key):
    data = load_json_file(file_path)
    interactions = defaultdict(int)
    for item in data.get(key, []):
        for entry in item.get('string_list_data', []):
            if 'href' in entry:
                interactions[entry['href']] += 1
    return interactions

def get_comments_interactions(file_path):
    data = load_json_file(file_path)
    interactions = defaultdict(int)
    for item in data.get('comments_reels_comments', []):
        for entry in item.get('string_map_data', {}).values():
            if 'href' in entry:
                interactions[entry['href']] += 1
    return interactions

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    post_likes_interactions = defaultdict(int)
    story_likes_interactions = defaultdict(int)
    comments_interactions = defaultdict(int)
    
    # Collect post likes interactions
    liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
    if os.path.exists(liked_posts_path):
        post_likes_interactions.update(get_interactions_from_file(liked_posts_path, 'likes_media_likes'))
    
    # Collect story likes interactions
    story_likes_path = os.path.join(root_dir, "story_interactions", "story_likes.json")
    if os.path.exists(story_likes_path):
        story_likes_interactions.update(get_interactions_from_file(story_likes_path, 'story_activities_story_likes'))
    
    # Collect comments interactions
    reels_comments_path = os.path.join(root_dir, "your_instagram_activity", "comments", "reels_comments.json")
    if os.path.exists(reels_comments_path):
        comments_interactions.update(get_comments_interactions(reels_comments_path))
    
    # Aggregate all interactions
    total_interactions = defaultdict(int)
    for interactions in [post_likes_interactions, story_likes_interactions, comments_interactions]:
        for user, count in interactions.items():
            total_interactions[user] += count
    
    # Sort by interaction count and get top 20
    top_interactions = sorted(total_interactions.items(), key=lambda x: x[1], reverse=True)[:20]
    
    # Prepare CSV output
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
        for user in top_interactions:
            post_likes = post_likes_interactions.get(user[0], 0)
            story_likes = story_likes_interactions.get(user[0], 0)
            comments = comments_interactions.get(user[0], 0)
            csvwriter.writerow([user[0], post_likes, story_likes, comments])

if __name__ == "__main__":
    main()
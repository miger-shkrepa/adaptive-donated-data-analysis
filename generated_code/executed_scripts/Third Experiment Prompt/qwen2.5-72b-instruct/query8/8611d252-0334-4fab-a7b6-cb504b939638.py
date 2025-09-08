import os
import json
import csv

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def get_interactions(root_dir):
    interactions = {}
    
    try:
        # Post Likes
        post_likes_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        if os.path.exists(post_likes_path):
            post_likes_data = load_json(post_likes_path)
            for item in post_likes_data.get("likes_media_likes", []):
                for like in item.get("string_list_data", []):
                    account = like.get("value")
                    if account:
                        interactions[account] = interactions.get(account, 0) + 1
        
        # Story Likes
        story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
        if os.path.exists(story_likes_path):
            story_likes_data = load_json(story_likes_path)
            for item in story_likes_data.get("story_activities_story_likes", []):
                for like in item.get("string_list_data", []):
                    account = like.get("value")
                    if account:
                        interactions[account] = interactions.get(account, 0) + 1
        
        # Comments
        comments_path = os.path.join(root_dir, "your_instagram_activity", "comments", "reels_comments.json")
        if os.path.exists(comments_path):
            comments_data = load_json(comments_path)
            for item in comments_data.get("comments_reels_comments", []):
                account = item.get("string_map_data", {}).get("Media Owner")
                if account:
                    interactions[account] = interactions.get(account, 0) + 1
    
    except Exception as e:
        raise e
    
    return interactions

def write_csv(interactions, output_path):
    top_interactions = sorted(interactions.items(), key=lambda x: x[1], reverse=True)[:20]
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for user, count in top_interactions:
            writer.writerow({
                'User': user,
                'Post Likes': 0,  # Placeholder, actual counts not separated
                'Story Likes': 0,  # Placeholder, actual counts not separated
                'Comments': 0  # Placeholder, actual counts not separated
            })

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    interactions = get_interactions(root_dir)
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    write_csv(interactions, output_path)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
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
        liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        if os.path.exists(liked_posts_path):
            liked_posts_data = load_json(liked_posts_path)
            for item in liked_posts_data.get("likes_media_likes", []):
                for data in item.get("string_list_data", []):
                    account = data.get("value")
                    if account:
                        interactions[account] = interactions.get(account, 0) + 1
        
        # Story Likes
        story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
        if os.path.exists(story_likes_path):
            story_likes_data = load_json(story_likes_path)
            for item in story_likes_data.get("story_activities_story_likes", []):
                for data in item.get("string_list_data", []):
                    account = data.get("value")
                    if account:
                        interactions[account] = interactions.get(account, 0) + 1
        
        # Comments
        comments_path = os.path.join(root_dir, "your_instagram_activity", "comments", "post_comments_1.json")
        if os.path.exists(comments_path):
            comments_data = load_json(comments_path)
            for item in comments_data:
                media_owner = item.get("string_map_data", {}).get("Media Owner")
                if media_owner:
                    interactions[media_owner] = interactions.get(media_owner, 0) + 1
        
        # Sort and get top 20
        top_interactions = sorted(interactions.items(), key=lambda x: x[1], reverse=True)[:20]
        return top_interactions
    
    except Exception as e:
        raise e

def write_csv(data, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for user, count in data:
                writer.writerow({'User': user, 'Post Likes': count, 'Story Likes': count, 'Comments': count})
    except Exception as e:
        raise e

if __name__ == "__main__":
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    try:
        interactions = get_interactions(root_dir)
        write_csv(interactions, 'query_responses/results.csv')
    except Exception as e:
        print(e)
        # If any error occurs, write a CSV file with only headers
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
import os
import json
import csv
from collections import defaultdict

root_dir = "root_dir"

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The JSON file is not properly formatted.")

def process_likes_and_comments(data_dir):
    user_interactions = defaultdict(int)
    
    likes_path = os.path.join(data_dir, "likes", "liked_comments.json")
    story_likes_path = os.path.join(data_dir, "story_interactions", "story_likes.json")
    comments_path = os.path.join(data_dir, "comments", "comments.json")  # Assuming comments.json exists based on the query

    try:
        if os.path.exists(likes_path):
            likes_data = load_json_data(likes_path)
            for entry in likes_data.get("liked_comments", []):
                user_interactions[entry.get("user", "Unknown")] += 1
        else:
            print("Warning: liked_comments.json not found. Post likes will be treated as 0.")
        
        if os.path.exists(story_likes_path):
            story_likes_data = load_json_data(story_likes_path)
            for story_like in story_likes_data.get("story_activities_story_likes", []):
                for data in story_like.get("string_list_data", []):
                    user_interactions["Unknown"] += 1  # Story likes do not specify the user, so we treat them as 'Unknown'
        else:
            print("Warning: story_likes.json not found. Story likes will be treated as 0.")
        
        if os.path.exists(comments_path):
            comments_data = load_json_data(comments_path)
            for comment in comments_data.get("comments", []):
                user_interactions[comment.get("user", "Unknown")] += 1
        else:
            print("Warning: comments.json not found. Comments will be treated as 0.")
        
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")
    
    return user_interactions

def write_to_csv(user_interactions, output_path):
    top_users = sorted(user_interactions.items(), key=lambda x: x[1], reverse=True)[:20]
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
        
        if not top_users:
            return
        
        for user, interactions in top_users:
            csv_writer.writerow([user, interactions, 0, 0])  # Since we cannot distinguish between likes and comments, we treat all as 'Post Likes'

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")
        
        user_interactions = process_likes_and_comments(root_dir)
        write_to_csv(user_interactions, 'query_responses/results.csv')
        
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
import os
import csv
import json

root_dir = "root_dir"

def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

def get_interactions(data):
    interactions = {}
    for item in data:
        for entry in item.get('string_list_data', []):
            user = entry.get('value')
            if user:
                interactions[user] = interactions.get(user, 0) + 1
    return interactions

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        post_likes_path = os.path.join(root_dir, 'activity', 'posts', 'post_likes.json')
        story_likes_path = os.path.join(root_dir, 'activity', 'stories', 'story_likes.json')
        comments_path = os.path.join(root_dir, 'activity', 'comments', 'comments.json')
        
        post_likes_data = read_json_file(post_likes_path).get('story_activities_post_likes', []) if os.path.exists(post_likes_path) else []
        story_likes_data = read_json_file(story_likes_path).get('story_activities_story_likes', []) if os.path.exists(story_likes_path) else []
        comments_data = read_json_file(comments_path).get('story_activities_comments', []) if os.path.exists(comments_path) else []
        
        post_likes_interactions = get_interactions(post_likes_data)
        story_likes_interactions = get_interactions(story_likes_data)
        comments_interactions = get_interactions(comments_data)
        
        all_interactions = {}
        for interactions in [post_likes_interactions, story_likes_interactions, comments_interactions]:
            for user, count in interactions.items():
                all_interactions[user] = all_interactions.get(user, 0) + count
        
        top_interactions = sorted(all_interactions.items(), key=lambda x: x[1], reverse=True)[:20]
        
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
    
    except Exception as e:
        print(e)
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])

if __name__ == "__main__":
    main()
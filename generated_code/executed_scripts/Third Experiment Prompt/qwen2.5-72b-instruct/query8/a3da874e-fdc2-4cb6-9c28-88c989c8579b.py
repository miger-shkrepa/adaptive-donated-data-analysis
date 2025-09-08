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
        post_likes_file = os.path.join(root_dir, 'your_instagram_activity', 'likes', 'liked_posts.json')
        if os.path.exists(post_likes_file):
            data = load_json(post_likes_file)
            for item in data.get('likes_media_likes', []):
                for string_data in item.get('string_list_data', []):
                    user = string_data.get('value')
                    if user:
                        interactions[user] = interactions.get(user, 0) + 1

        # Story Likes
        story_likes_file = os.path.join(root_dir, 'your_instagram_activity', 'story_interactions', 'story_likes.json')
        if os.path.exists(story_likes_file):
            data = load_json(story_likes_file)
            for item in data.get('story_activities_story_likes', []):
                for string_data in item.get('string_list_data', []):
                    if 'value' in string_data:
                        user = string_data.get('value')
                        if user:
                            interactions[user] = interactions.get(user, 0) + 1

        # Comments
        comments_file = os.path.join(root_dir, 'your_instagram_activity', 'comments', 'post_comments_1.json')
        if os.path.exists(comments_file):
            data = load_json(comments_file)
            for item in data:
                media_owner = item.get('string_map_data', {}).get('Media Owner', {}).get('value')
                if media_owner:
                    interactions[media_owner] = interactions.get(media_owner, 0) + 1

    except Exception as e:
        print(f"Error: {e}")
    
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
                'Post Likes': 0,  # Placeholder, actual counts not available
                'Story Likes': 0,  # Placeholder, actual counts not available
                'Comments': 0  # Placeholder, actual counts not available
            })

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    interactions = get_interactions(root_dir)
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    write_csv(interactions, output_path)

if __name__ == "__main__":
    main()
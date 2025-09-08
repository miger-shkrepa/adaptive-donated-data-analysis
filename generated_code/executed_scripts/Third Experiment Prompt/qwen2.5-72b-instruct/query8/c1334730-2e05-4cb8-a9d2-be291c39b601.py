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

    # Post Likes
    post_likes_path = os.path.join(root_dir, 'your_instagram_activity', 'likes', 'liked_posts.json')
    if os.path.exists(post_likes_path):
        try:
            data = load_json(post_likes_path)
            for item in data.get('likes_media_likes', []):
                for string_data in item.get('string_list_data', []):
                    account = string_data.get('value')
                    if account:
                        interactions[account] = interactions.get(account, 0) + 1
        except Exception as e:
            print(f"Error processing {post_likes_path}: {e}")

    # Story Likes
    story_likes_path = os.path.join(root_dir, 'your_instagram_activity', 'story_interactions', 'story_likes.json')
    if os.path.exists(story_likes_path):
        try:
            data = load_json(story_likes_path)
            for item in data.get('story_activities_story_likes', []):
                for string_data in item.get('string_list_data', []):
                    interactions[string_data.get('value', '')] = interactions.get(string_data.get('value', ''), 0) + 1
        except Exception as e:
            print(f"Error processing {story_likes_path}: {e}")

    # Comments
    comments_path = os.path.join(root_dir, 'your_instagram_activity', 'comments', 'post_comments_1.json')
    if os.path.exists(comments_path):
        try:
            data = load_json(comments_path)
            for item in data:
                media_owner = item.get('string_map_data', {}).get('Media Owner', {}).get('value')
                if media_owner:
                    interactions[media_owner] = interactions.get(media_owner, 0) + 1
        except Exception as e:
            print(f"Error processing {comments_path}: {e}")

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
                'Post Likes': count,
                'Story Likes': 0,
                'Comments': 0
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
import os
import json
import csv

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def get_interactions(file_path, interaction_type):
    try:
        data = load_json_file(file_path)
        interactions = {}
        if interaction_type == 'post_likes':
            for item in data.get('likes_media_likes', []):
                for media in item.get('string_list_data', []):
                    account = media.get('value')
                    if account:
                        interactions[account] = interactions.get(account, 0) + 1
        elif interaction_type == 'story_likes':
            for item in data.get('story_activities_story_likes', []):
                for media in item.get('string_list_data', []):
                    interactions[media.get('value', '')] = interactions.get(media.get('value', ''), 0) + 1
        elif interaction_type == 'comments':
            for item in data.get('comments_reels_comments', []):
                account = item.get('string_map_data', {}).get('Media Owner', {}).get('value')
                if account:
                    interactions[account] = interactions.get(account, 0) + 1
        return interactions
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return {}

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        post_likes_file = os.path.join(root_dir, 'your_instagram_activity', 'likes', 'liked_posts.json')
        story_likes_file = os.path.join(root_dir, 'your_instagram_activity', 'story_interactions', 'story_likes.json')
        comments_file = os.path.join(root_dir, 'your_instagram_activity', 'comments', 'reels_comments.json')

        post_likes = get_interactions(post_likes_file, 'post_likes')
        story_likes = get_interactions(story_likes_file, 'story_likes')
        comments = get_interactions(comments_file, 'comments')

        interactions = {}
        for account in set(list(post_likes.keys()) + list(story_likes.keys()) + list(comments.keys())):
            interactions[account] = {
                'Post Likes': post_likes.get(account, 0),
                'Story Likes': story_likes.get(account, 0),
                'Comments': comments.get(account, 0)
            }

        sorted_interactions = sorted(interactions.items(), key=lambda x: sum(x[1].values()), reverse=True)[:20]

        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for account, data in sorted_interactions:
                row = {'User': account}
                row.update(data)
                writer.writerow(row)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
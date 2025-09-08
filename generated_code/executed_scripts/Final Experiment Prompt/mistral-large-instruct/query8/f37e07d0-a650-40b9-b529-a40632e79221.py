import os
import json
import csv

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON.")

def count_interactions(data, key, interaction_type):
    counts = {}
    for item in data.get(key, []):
        if interaction_type == 'Post Likes':
            title = item.get('title', '')
        elif interaction_type == 'Story Likes':
            title = item.get('title', '')
        elif interaction_type == 'Comments':
            title = item.get('string_map_data', {}).get('Media Owner', {}).get('value', '')
        else:
            continue

        if title:
            counts[title] = counts.get(title, 0) + 1
    return counts

def main():
    try:
        liked_posts_path = os.path.join(root_dir, 'your_instagram_activity', 'likes', 'liked_posts.json')
        story_likes_path = os.path.join(root_dir, 'your_instagram_activity', 'story_interactions', 'story_likes.json')
        reels_comments_path = os.path.join(root_dir, 'your_instagram_activity', 'comments', 'reels_comments.json')

        liked_posts_data = load_json(liked_posts_path)
        story_likes_data = load_json(story_likes_path)
        reels_comments_data = load_json(reels_comments_path)

        post_likes = count_interactions(liked_posts_data, 'likes_media_likes', 'Post Likes')
        story_likes = count_interactions(story_likes_data, 'story_activities_story_likes', 'Story Likes')
        comments = count_interactions(reels_comments_data, 'comments_reels_comments', 'Comments')

        combined_counts = {}
        for user in set(post_likes.keys()).union(story_likes.keys()).union(comments.keys()):
            combined_counts[user] = {
                'Post Likes': post_likes.get(user, 0),
                'Story Likes': story_likes.get(user, 0),
                'Comments': comments.get(user, 0)
            }

        sorted_users = sorted(combined_counts.items(), key=lambda x: sum(x[1].values()), reverse=True)[:20]

        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', newline='') as csvfile:
            fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for user, counts in sorted_users:
                writer.writerow({
                    'User': user,
                    'Post Likes': counts['Post Likes'],
                    'Story Likes': counts['Story Likes'],
                    'Comments': counts['Comments']
                })

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
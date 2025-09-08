import os
import json
import csv
from collections import Counter

root_dir = "root_dir"

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The JSON file is not properly formatted.")

def get_top_interactions(data, interaction_type):
    interactions = Counter()
    for media_like in data.get(interaction_type, []):
        for string_data in media_like.get('string_list_data', []):
            value = string_data.get('value')
            if value:
                interactions[value] += 1
    return interactions.most_common(20)

def process_data():
    try:
        liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        liked_posts_data = load_json_data(liked_posts_path)
        post_likes = get_top_interactions(liked_posts_data['structure'], 'likes_media_likes')

        # Assuming story likes and comments are not available in the given structure
        story_likes = []
        comments = []

        return post_likes, story_likes, comments
    except FileNotFoundError as e:
        print(e)
        return [], [], []

def write_to_csv(post_likes, story_likes, comments):
    file_path = 'query_responses/results.csv'
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
            for i in range(20):
                user = post_likes[i][0] if i < len(post_likes) else ''
                post_like_count = post_likes[i][1] if i < len(post_likes) else 0
                story_like_count = story_likes[i][1] if i < len(story_likes) else 0
                comment_count = comments[i][1] if i < len(comments) else 0
                csvwriter.writerow([user, post_like_count, story_like_count, comment_count])
    except Exception as e:
        raise Exception(f"Error: Failed to write to CSV file. Reason: {str(e)}")

def main():
    post_likes, story_likes, comments = process_data()
    write_to_csv(post_likes, story_likes, comments)

if __name__ == "__main__":
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        main()
    except Exception as e:
        print(e)
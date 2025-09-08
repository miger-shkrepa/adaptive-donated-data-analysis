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

def process_data():
    user_interactions = defaultdict(int)
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")

        # Process story likes
        story_likes_path = os.path.join(root_dir, "story_interactions", "story_likes.json")
        if os.path.exists(story_likes_path):
            story_likes_data = load_json_data(story_likes_path)
            for story_like in story_likes_data.get("story_activities_story_likes", []):
                for data in story_like.get("string_list_data", []):
                    user_interactions[data.get("value", "")] += 1

        # Process post likes (assuming this data is not directly provided in the given structure)
        post_likes_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        if os.path.exists(post_likes_path):
            post_likes_data = load_json_data(post_likes_path)
            for post_like in post_likes_data.get("impressions_history_posts_seen", []):
                author = post_like.get("string_map_data", {}).get("Author", {}).get("value")
                if author:
                    user_interactions[author] += 1

        # Process comments (assuming this data is not directly provided in the given structure)
        # Since there is no direct mention of comments in the provided structure, treat its contribution as 0.

        # Get top 20 interactions
        top_interactions = sorted(user_interactions.items(), key=lambda x: x[1], reverse=True)[:20]

        return top_interactions

    except Exception as e:
        raise e

def write_to_csv(data):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user, count in data:
            writer.writerow({'User': user, 'Post Likes': 0, 'Story Likes': count, 'Comments': 0})

try:
    top_interactions = process_data()
    write_to_csv(top_interactions)
except Exception as e:
    print(e)
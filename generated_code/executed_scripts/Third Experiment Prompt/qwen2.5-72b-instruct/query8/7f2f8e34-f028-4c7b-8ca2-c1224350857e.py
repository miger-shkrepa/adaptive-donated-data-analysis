import os
import json
import csv

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The JSON file is not properly formatted.")

def get_top_interactions(root_dir):
    interactions = {}
    try:
        liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        if os.path.exists(liked_posts_path):
            liked_posts_data = load_json(liked_posts_path)
            for like in liked_posts_data.get("likes_media_likes", []):
                for string_data in like.get("string_list_data", []):
                    value = string_data.get("value")
                    if value:
                        interactions[value] = interactions.get(value, 0) + 1

        saved_posts_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")
        if os.path.exists(saved_posts_path):
            saved_posts_data = load_json(saved_posts_path)
            for saved in saved_posts_data.get("saved_saved_media", []):
                title = saved.get("title")
                if title:
                    interactions[title] = interactions.get(title, 0) + 1

        # Sort interactions by count in descending order and take top 20
        top_interactions = sorted(interactions.items(), key=lambda x: x[1], reverse=True)[:20]
        return top_interactions

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def write_to_csv(data, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for user, count in data:
                writer.writerow({'User': user, 'Post Likes': count, 'Story Likes': 0, 'Comments': 0})
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

if __name__ == "__main__":
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    try:
        top_interactions = get_top_interactions(root_dir)
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        write_to_csv(top_interactions, output_path)
    except Exception as e:
        print(str(e))
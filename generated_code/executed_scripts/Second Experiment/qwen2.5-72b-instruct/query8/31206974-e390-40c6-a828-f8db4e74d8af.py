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

def process_data(root_dir):
    user_interactions = {}
    try:
        liked_posts_path = os.path.join(root_dir, "likes", "liked_posts.json")
        if os.path.exists(liked_posts_path):
            liked_posts_data = load_json(liked_posts_path)
            for post in liked_posts_data.get("likes_media_likes", []):
                for like in post.get("string_list_data", []):
                    user = like.get("value")
                    if user:
                        user_interactions[user] = user_interactions.get(user, 0) + 1

        for dirpath, dirnames, filenames in os.walk(os.path.join(root_dir, "messages", "inbox")):
            for filename in filenames:
                if filename.endswith(".json"):
                    message_file_path = os.path.join(dirpath, filename)
                    message_data = load_json(message_file_path)
                    for message in message_data.get("messages", []):
                        sender_name = message.get("sender_name")
                        if sender_name:
                            user_interactions[sender_name] = user_interactions.get(sender_name, 0) + 1

        sorted_interactions = sorted(user_interactions.items(), key=lambda x: x[1], reverse=True)[:20]
        return sorted_interactions
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def write_to_csv(data, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            if data:
                for user, count in data:
                    writer.writerow({'User': user, 'Post Likes': count, 'Story Likes': 0, 'Comments': 0})
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

if __name__ == "__main__":
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    try:
        interactions = process_data(root_dir)
        write_to_csv(interactions, 'query_responses/results.csv')
    except Exception as e:
        print(str(e))
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
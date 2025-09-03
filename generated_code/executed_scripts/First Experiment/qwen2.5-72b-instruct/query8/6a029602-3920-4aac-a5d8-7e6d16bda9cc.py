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

def process_likes_and_comments(root_dir):
    user_interactions = defaultdict(int)
    try:
        for dirpath, _, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename == "liked_posts.json":
                    file_path = os.path.join(dirpath, filename)
                    data = load_json_data(file_path)
                    for item in data.get("likes_media_likes", []):
                        for like in item.get("string_list_data", []):
                            user_interactions[like.get("value")] += 1

                elif filename == "message_1.json":
                    file_path = os.path.join(dirpath, filename)
                    data = load_json_data(file_path)
                    for message in data.get("messages", []):
                        if "sender_name" in message:
                            user_interactions[message["sender_name"]] += 1

        sorted_interactions = sorted(user_interactions.items(), key=lambda x: x[1], reverse=True)[:20]
        return sorted_interactions
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while processing the data. {str(e)}")

def write_to_csv(data):
    try:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for user, count in data:
                writer.writerow({'User': user, 'Post Likes': count, 'Story Likes': 0, 'Comments': 0})
    except Exception as e:
        raise Exception(f"Error: An error occurred while writing to the CSV file. {str(e)}")

if __name__ == "__main__":
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")
    try:
        interactions = process_likes_and_comments(root_dir)
        write_to_csv(interactions)
    except Exception as e:
        print(str(e))
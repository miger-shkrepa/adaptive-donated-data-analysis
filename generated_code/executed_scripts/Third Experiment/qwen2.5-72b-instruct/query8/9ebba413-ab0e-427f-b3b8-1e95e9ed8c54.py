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

def process_likes_comments(directory):
    interaction_counts = defaultdict(int)
    likes_files = ["liked_comments.json", "liked_posts.json"]
    comments_files = ["message_1.json"]

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file in likes_files:
                file_path = os.path.join(root, file)
                data = load_json_data(file_path)
                likes_data = data.get("likes_comment_likes", []) + data.get("likes_media_likes", [])
                for item in likes_data:
                    for string_data in item.get("string_list_data", []):
                        value = string_data.get("value")
                        if value:
                            interaction_counts[value] += 1

            if file in comments_files:
                file_path = os.path.join(root, file)
                data = load_json_data(file_path)
                messages = data.get("messages", [])
                for message in messages:
                    sender_name = message.get("sender_name")
                    if sender_name:
                        interaction_counts[sender_name] += 1

    return interaction_counts

def write_to_csv(interaction_counts, output_path):
    sorted_interactions = sorted(interaction_counts.items(), key=lambda x: x[1], reverse=True)[:20]
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
        for user, count in sorted_interactions:
            writer.writerow([user, count, 0, 0])  # Assuming story likes and comments are not separately counted

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    interaction_counts = process_likes_comments(os.path.join(root_dir, "likes"))
    write_to_csv(interaction_counts, 'query_responses/results.csv')
except Exception as e:
    print(e)
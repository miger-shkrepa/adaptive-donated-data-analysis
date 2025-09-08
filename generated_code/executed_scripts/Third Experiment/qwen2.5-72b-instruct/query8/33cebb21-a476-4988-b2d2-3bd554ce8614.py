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

def process_likes_comments(directory):
    likes_comments = Counter()
    try:
        liked_posts = load_json_data(os.path.join(directory, 'likes', 'liked_posts.json'))
        for item in liked_posts.get('likes_media_likes', []):
            for data in item.get('string_list_data', []):
                likes_comments[data['value']] += 1

        liked_comments = load_json_data(os.path.join(directory, 'likes', 'liked_comments.json'))
        for item in liked_comments.get('likes_comment_likes', []):
            for data in item.get('string_list_data', []):
                likes_comments[data['value']] += 1

        story_likes = load_json_data(os.path.join(directory, 'story_interactions', 'story_likes.json'))
        for item in story_likes.get('story_activities_story_likes', []):
            likes_comments[item['title']] += 1

    except FileNotFoundError:
        pass  # If any of the files are missing, treat their contribution as 0 and continue

    return likes_comments

def process_messages(directory):
    message_interactions = Counter()
    try:
        inbox_dir = os.path.join(directory, 'messages', 'inbox')
        if os.path.exists(inbox_dir):
            for username in os.listdir(inbox_dir):
                message_file = os.path.join(inbox_dir, username, 'message_1.json')
                messages = load_json_data(message_file)
                for message in messages.get('messages', []):
                    message_interactions[message['sender_name']] += 1

        message_requests_dir = os.path.join(directory, 'messages', 'message_requests')
        if os.path.exists(message_requests_dir):
            for request in os.listdir(message_requests_dir):
                message_file = os.path.join(message_requests_dir, request, 'message_1.json')
                messages = load_json_data(message_file)
                for message in messages.get('messages', []):
                    message_interactions[message['sender_name']] += 1

    except FileNotFoundError:
        pass  # If any of the files are missing, treat their contribution as 0 and continue

    return message_interactions

def generate_csv(data, file_path):
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['User', 'Post Likes', 'Story Likes and Comments']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user, count in data.most_common(20):
            writer.writerow({'User': user, 'Post Likes': count, 'Story Likes and Comments': 0})

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    likes_comments = process_likes_comments(root_dir)
    message_interactions = process_messages(root_dir)

    combined_interactions = likes_comments + message_interactions

    generate_csv(combined_interactions, 'query_responses/results.csv')

except Exception as e:
    print(e)
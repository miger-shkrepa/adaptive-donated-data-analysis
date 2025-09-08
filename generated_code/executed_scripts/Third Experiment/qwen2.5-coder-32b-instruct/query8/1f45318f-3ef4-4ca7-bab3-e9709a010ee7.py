import os
import csv
from collections import defaultdict

root_dir = "root_dir"

def get_likes_and_comments_data(root_dir):
    likes_data = defaultdict(int)
    comments_data = defaultdict(int)

    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    # Check for likes data
    likes_dir = os.path.join(root_dir, "personal_information", "likes")
    if os.path.exists(likes_dir):
        liked_posts_path = os.path.join(likes_dir, "liked_posts.json")
        if os.path.exists(liked_posts_path):
            with open(liked_posts_path, 'r') as file:
                import json
                liked_posts = json.load(file)
                for like in liked_posts.get('likes_media_likes', []):
                    for item in like.get('string_list_data', []):
                        likes_data[item.get('value')] += 1

        liked_comments_path = os.path.join(likes_dir, "liked_comments.json")
        if os.path.exists(liked_comments_path):
            with open(liked_comments_path, 'r') as file:
                import json
                liked_comments = json.load(file)
                for like in liked_comments.get('likes_comment_likes', []):
                    for item in like.get('string_list_data', []):
                        comments_data[item.get('value')] += 1

    # Check for messages data
    messages_dir = os.path.join(root_dir, "personal_information", "messages", "inbox")
    if os.path.exists(messages_dir):
        for user_dir in os.listdir(messages_dir):
            user_path = os.path.join(messages_dir, user_dir)
            if os.path.isdir(user_path):
                for message_file in os.listdir(user_path):
                    if message_file.endswith('.json'):
                        message_path = os.path.join(user_path, message_file)
                        with open(message_path, 'r') as file:
                            import json
                            messages = json.load(file)
                            for message in messages.get('messages', []):
                                comments_data[message.get('sender_name')] += 1

    return likes_data, comments_data

def aggregate_data(likes_data, comments_data):
    interaction_data = defaultdict(int)
    for user, count in likes_data.items():
        interaction_data[user] += count
    for user, count in comments_data.items():
        interaction_data[user] += count
    return interaction_data

def write_to_csv(interaction_data):
    sorted_interactions = sorted(interaction_data.items(), key=lambda x: x[1], reverse=True)[:20]
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['User', 'Post Likes', 'Story Likes and Comments'])
        for user, total_interactions in sorted_interactions:
            csvwriter.writerow([user, likes_data.get(user, 0), comments_data.get(user, 0)])

try:
    likes_data, comments_data = get_likes_and_comments_data(root_dir)
    interaction_data = aggregate_data(likes_data, comments_data)
    write_to_csv(interaction_data)
except FileNotFoundError as e:
    print(e)
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['User', 'Post Likes', 'Story Likes and Comments'])
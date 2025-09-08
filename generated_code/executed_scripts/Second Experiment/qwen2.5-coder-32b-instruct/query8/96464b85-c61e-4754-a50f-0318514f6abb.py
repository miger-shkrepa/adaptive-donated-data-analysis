import os
import csv
import json

root_dir = "root_dir"

def get_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

def process_likes_data(data):
    likes = {}
    for item in data.get('likes_media_likes', []):
        for string_data in item.get('string_list_data', []):
            if 'href' in string_data:
                user = string_data['href']
                likes[user] = likes.get(user, 0) + 1
    return likes

def process_comments_data(data):
    comments = {}
    for message in data.get('messages', []):
        if 'sender_name' in message:
            user = message['sender_name']
            comments[user] = comments.get(user, 0) + 1
    return comments

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        likes_data = {}
        comments_data = {}

        # Process likes data
        likes_path = os.path.join(root_dir, 'likes', 'liked_posts.json')
        if os.path.exists(likes_path):
            likes_json = get_json_data(likes_path)
            likes_data = process_likes_data(likes_json)

        # Process comments data
        messages_dir = os.path.join(root_dir, 'messages', 'inbox')
        if os.path.exists(messages_dir):
            for username in os.listdir(messages_dir):
                user_dir = os.path.join(messages_dir, username)
                if os.path.isdir(user_dir):
                    for message_file in os.listdir(user_dir):
                        if message_file.endswith('.json'):
                            message_path = os.path.join(user_dir, message_file)
                            message_json = get_json_data(message_path)
                            comments_data.update(process_comments_data(message_json))

        # Aggregate data
        interaction_counts = {}
        for user, count in likes_data.items():
            interaction_counts[user] = interaction_counts.get(user, 0) + count
        for user, count in comments_data.items():
            interaction_counts[user] = interaction_counts.get(user, 0) + count

        # Sort by interaction count
        sorted_interactions = sorted(interaction_counts.items(), key=lambda x: x[1], reverse=True)[:20]

        # Write to CSV
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['User', 'Post Likes', 'Story Likes and Comments'])
            for user, count in sorted_interactions:
                csvwriter.writerow([user, likes_data.get(user, 0), comments_data.get(user, 0)])

    except Exception as e:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['User', 'Post Likes', 'Story Likes and Comments'])

if __name__ == "__main__":
    main()
import os
import csv
import json

root_dir = "root_dir"

def get_file_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

def aggregate_likes_and_comments(root_dir):
    interactions = {}

    # Collecting post likes
    liked_posts_path = os.path.join(root_dir, 'likes', 'liked_posts.json')
    if os.path.exists(liked_posts_path):
        liked_posts_data = get_file_data(liked_posts_path)
        for like in liked_posts_data.get('likes_media_likes', []):
            for data in like.get('string_list_data', []):
                user = data.get('value')
                if user:
                    interactions[user] = interactions.get(user, 0) + 1

    # Collecting story likes and comments
    story_likes_path = os.path.join(root_dir, 'story_activities', 'story_likes.json')
    if os.path.exists(story_likes_path):
        story_likes_data = get_file_data(story_likes_path)
        for like in story_likes_data.get('story_activities_story_likes', []):
            for data in like.get('string_list_data', []):
                user = data.get('value')
                if user:
                    interactions[user] = interactions.get(user, 0) + 1

    # Collecting comments
    inbox_path = os.path.join(root_dir, 'messages', 'inbox')
    if os.path.exists(inbox_path):
        for username in os.listdir(inbox_path):
            user_messages_path = os.path.join(inbox_path, username)
            for message_file in os.listdir(user_messages_path):
                message_data = get_file_data(os.path.join(user_messages_path, message_file))
                for message in message_data.get('messages', []):
                    sender = message.get('sender_name')
                    if sender:
                        interactions[sender] = interactions.get(sender, 0) + 1

    return interactions

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        interactions = aggregate_likes_and_comments(root_dir)

        # Sorting interactions by count in descending order and getting top 20
        top_interactions = sorted(interactions.items(), key=lambda x: x[1], reverse=True)[:20]

        # Writing to CSV
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['User', 'Post Likes', 'Story Likes and Comments'])
            for user, count in top_interactions:
                csvwriter.writerow([user, count, count])

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
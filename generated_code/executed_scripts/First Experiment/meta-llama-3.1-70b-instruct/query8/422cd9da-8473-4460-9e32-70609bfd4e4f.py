import os
import json
import csv
from collections import defaultdict

root_dir = "root_dir"

def get_interacted_accounts(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize dictionaries to store interaction counts
        post_likes = defaultdict(int)
        story_likes = defaultdict(int)
        comments = defaultdict(int)

        # Iterate over the 'likes' directory
        likes_dir = os.path.join(root_dir, 'likes')
        if os.path.exists(likes_dir):
            for filename in os.listdir(likes_dir):
                if filename == 'liked_posts.json':
                    with open(os.path.join(likes_dir, filename), 'r') as f:
                        data = json.load(f)
                        for item in data['likes_media_likes']:
                            for string_data in item['string_list_data']:
                                post_likes[string_data['value']] += 1
                elif filename == 'liked_comments.json':
                    with open(os.path.join(likes_dir, filename), 'r') as f:
                        data = json.load(f)
                        for item in data['likes_comment_likes']:
                            for string_data in item['string_list_data']:
                                comments[string_data['value']] += 1

        # Iterate over the 'messages' directory
        messages_dir = os.path.join(root_dir, 'messages')
        if os.path.exists(messages_dir):
            for filename in os.listdir(os.path.join(messages_dir, 'inbox', 'conversation')):
                if filename.endswith('.json'):
                    with open(os.path.join(messages_dir, 'inbox', 'conversation', filename), 'r') as f:
                        data = json.load(f)
                        for message in data['messages']:
                            if 'sender_name' in message:
                                comments[message['sender_name']] += 1

        # Combine interaction counts
        interaction_counts = {}
        for account in set(list(post_likes.keys()) + list(story_likes.keys()) + list(comments.keys())):
            interaction_counts[account] = post_likes[account] + story_likes[account] + comments[account]

        # Get top 20 interacted accounts
        top_20_accounts = sorted(interaction_counts.items(), key=lambda x: x[1], reverse=True)[:20]

        return top_20_accounts

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(accounts):
    try:
        with open('query_responses/results.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
            for account, count in accounts:
                writer.writerow([account, 0, 0, count])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        accounts = get_interacted_accounts(root_dir)
        save_to_csv(accounts)

    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: " + str(e))
    except ValueError as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()
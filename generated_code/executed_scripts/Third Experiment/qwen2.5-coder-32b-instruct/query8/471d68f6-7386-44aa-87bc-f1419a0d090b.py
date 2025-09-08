import os
import csv
import json

root_dir = "root_dir"

def get_user_interactions(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        interactions = {}
        
        # Collecting post likes from subscriptions/reels.json
        reels_path = os.path.join(root_dir, "subscriptions", "reels.json")
        if os.path.exists(reels_path):
            with open(reels_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for item in data.get('subscriptions_reels', []):
                    username = item['string_map_data'].get('Benutzername', {}).get('value')
                    if username:
                        interactions[username] = interactions.get(username, 0) + 1
        
        # Collecting story likes from story_interactions/story_likes.json
        story_likes_path = os.path.join(root_dir, "story_interactions", "story_likes.json")
        if os.path.exists(story_likes_path):
            with open(story_likes_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for item in data.get('story_activities_story_likes', []):
                    for string_data in item.get('string_list_data', []):
                        username = string_data.get('value')
                        if username:
                            interactions[username] = interactions.get(username, 0) + 1
        
        # Collecting comments from messages/inbox and messages/message_requests
        messages_dir = os.path.join(root_dir, "messages", "inbox")
        if os.path.exists(messages_dir):
            for user_dir in os.listdir(messages_dir):
                user_path = os.path.join(messages_dir, user_dir)
                for message_file in os.listdir(user_path):
                    if message_file.endswith('.json'):
                        with open(os.path.join(user_path, message_file), 'r', encoding='utf-8') as file:
                            data = json.load(file)
                            for message in data['structure'].get('messages', []):
                                sender_name = message.get('sender_name')
                                if sender_name:
                                    interactions[sender_name] = interactions.get(sender_name, 0) + 1
        
        message_requests_dir = os.path.join(root_dir, "messages", "message_requests")
        if os.path.exists(message_requests_dir):
            for user_dir in os.listdir(message_requests_dir):
                user_path = os.path.join(message_requests_dir, user_dir)
                for message_file in os.listdir(user_path):
                    if message_file.endswith('.json'):
                        with open(os.path.join(user_path, message_file), 'r', encoding='utf-8') as file:
                            data = json.load(file)
                            for message in data['structure'].get('messages', []):
                                sender_name = message.get('sender_name')
                                if sender_name:
                                    interactions[sender_name] = interactions.get(sender_name, 0) + 1
        
        # Sorting interactions by count in descending order
        sorted_interactions = sorted(interactions.items(), key=lambda x: x[1], reverse=True)[:20]
        
        # Writing to CSV
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['User', 'Post Likes', 'Story Likes and Comments'])
            for user, count in sorted_interactions:
                csvwriter.writerow([user, 0, count])
    
    except Exception as e:
        print(f"Error: {str(e)}")
        # Writing only headers to CSV if an error occurs
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['User', 'Post Likes', 'Story Likes and Comments'])

get_user_interactions(root_dir)
import os
import csv
import json

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

def get_likes_data(root_dir):
    likes_data = {}
    likes_dir = os.path.join(root_dir, 'likes')
    
    if not os.path.exists(likes_dir):
        return likes_data
    
    liked_comments_path = os.path.join(likes_dir, 'liked_comments.json')
    liked_posts_path = os.path.join(likes_dir, 'liked_posts.json')
    
    if os.path.exists(liked_comments_path):
        liked_comments_data = load_json_file(liked_comments_path)
        for item in liked_comments_data.get('likes_comment_likes', []):
            for data in item.get('string_list_data', []):
                if 'href' in data:
                    account = data['href']
                    likes_data[account] = likes_data.get(account, 0) + 1
    
    if os.path.exists(liked_posts_path):
        liked_posts_data = load_json_file(liked_posts_path)
        for item in liked_posts_data.get('likes_media_likes', []):
            for data in item.get('string_list_data', []):
                if 'href' in data:
                    account = data['href']
                    likes_data[account] = likes_data.get(account, 0) + 1
    
    return likes_data

def get_story_likes_data(root_dir):
    story_likes_data = {}
    story_likes_path = os.path.join(root_dir, 'story_interactions', 'story_likes.json')
    
    if not os.path.exists(story_likes_path):
        return story_likes_data
    
    story_likes_data_json = load_json_file(story_likes_path)
    for item in story_likes_data_json.get('story_activities_story_likes', []):
        for data in item.get('string_list_data', []):
            if 'href' in data:
                account = data['href']
                story_likes_data[account] = story_likes_data.get(account, 0) + 1
    
    return story_likes_data

def get_comments_data(root_dir):
    comments_data = {}
    messages_dir = os.path.join(root_dir, 'messages', 'inbox')
    
    if not os.path.exists(messages_dir):
        return comments_data
    
    for username in os.listdir(messages_dir):
        user_dir = os.path.join(messages_dir, username)
        for message_file in os.listdir(user_dir):
            if message_file.endswith('.json'):
                message_data = load_json_file(os.path.join(user_dir, message_file))
                for message in message_data.get('messages', []):
                    if 'sender_name' in message:
                        account = message['sender_name']
                        comments_data[account] = comments_data.get(account, 0) + 1
    
    return comments_data

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    likes_data = get_likes_data(root_dir)
    story_likes_data = get_story_likes_data(root_dir)
    comments_data = get_comments_data(root_dir)
    
    interaction_counts = {}
    
    for account, count in likes_data.items():
        interaction_counts[account] = interaction_counts.get(account, 0) + count
    
    for account, count in story_likes_data.items():
        interaction_counts[account] = interaction_counts.get(account, 0) + count
    
    for account, count in comments_data.items():
        interaction_counts[account] = interaction_counts.get(account, 0) + count
    
    sorted_interactions = sorted(interaction_counts.items(), key=lambda x: x[1], reverse=True)[:20]
    
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['User', 'Post Likes', 'Story Likes and Comments'])
        for account, total_interactions in sorted_interactions:
            post_likes = likes_data.get(account, 0)
            story_likes_comments = story_likes_data.get(account, 0) + comments_data.get(account, 0)
            csvwriter.writerow([account, post_likes, story_likes_comments])

if __name__ == "__main__":
    main()
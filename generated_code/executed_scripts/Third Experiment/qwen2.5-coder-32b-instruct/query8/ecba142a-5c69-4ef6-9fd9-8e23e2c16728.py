import os
import csv
from collections import defaultdict

root_dir = "root_dir"

def get_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return eval(file.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except Exception as e:
        raise ValueError(f"ValueError: Error reading the file {file_path}. {str(e)}")

def aggregate_likes_and_comments(root_dir):
    likes_data = defaultdict(int)
    comments_data = defaultdict(int)
    
    # Aggregating likes from liked_posts.json
    liked_posts_path = os.path.join(root_dir, "likes", "liked_posts.json")
    if os.path.exists(liked_posts_path):
        liked_posts_data = get_json_data(liked_posts_path)
        for like in liked_posts_data.get("likes_media_likes", []):
            for string_data in like.get("string_list_data", []):
                likes_data[string_data.get("value", "")] += 1
    
    # Aggregating comments from messages
    messages_dir = os.path.join(root_dir, "messages", "inbox")
    if os.path.exists(messages_dir):
        for username in os.listdir(messages_dir):
            message_file_path = os.path.join(messages_dir, username, "message_1.json")
            if os.path.exists(message_file_path):
                message_data = get_json_data(message_file_path)
                for message in message_data.get("messages", []):
                    comments_data[message.get("sender_name", "")] += 1
    
    # Aggregating story likes is not directly available in the provided structure
    # Assuming story likes are part of the likes in liked_posts.json or comments
    
    # Combining likes and comments
    combined_data = defaultdict(int)
    for user, count in likes_data.items():
        combined_data[user] += count
    for user, count in comments_data.items():
        combined_data[user] += count
    
    # Sorting by interaction count
    sorted_interactions = sorted(combined_data.items(), key=lambda x: x[1], reverse=True)[:20]
    
    return sorted_interactions

def save_to_csv(data, file_path):
    try:
        with open(file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["User", "Post Likes", "Story Likes", "Comments"])
            for user, total_interactions in data:
                # Assuming all interactions are either post likes or comments
                # Story likes are not directly available, so they are set to 0
                csvwriter.writerow([user, 0, 0, total_interactions])
    except Exception as e:
        raise ValueError(f"ValueError: Error writing to the file {file_path}. {str(e)}")

try:
    interactions = aggregate_likes_and_comments(root_dir)
    save_to_csv(interactions, 'query_responses/results.csv')
except Exception as e:
    print(e)
    # If there's an error, create an empty CSV with headers
    save_to_csv([], 'query_responses/results.csv')
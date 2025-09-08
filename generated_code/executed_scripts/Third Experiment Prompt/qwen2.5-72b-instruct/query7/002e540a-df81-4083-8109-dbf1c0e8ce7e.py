import os
import json
import csv
from collections import Counter

root_dir = "root_dir"

def process_data(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        
        if not os.path.exists(liked_posts_path):
            print("Warning: liked_posts.json does not exist. Returning an empty CSV file.")
            with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['User', 'Times Engaged'])
            return
        
        with open(liked_posts_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        
        if 'likes_media_likes' not in data:
            raise ValueError("Error: Invalid JSON structure. 'likes_media_likes' key not found.")
        
        usernames = []
        for item in data['likes_media_likes']:
            for string_list_data in item.get('string_list_data', []):
                if 'value' in string_list_data:
                    usernames.append(string_list_data['value'])
        
        username_counts = Counter(usernames)
        
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['User', 'Times Engaged'])
            for username, count in username_counts.items():
                writer.writerow([username, count])
    
    except FileNotFoundError as e:
        print(e)
    except json.JSONDecodeError as e:
        print(f"Error: JSON decoding error. {e}")
    except Exception as e:
        print(f"Error: {e}")

process_data(root_dir)
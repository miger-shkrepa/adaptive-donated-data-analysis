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

def process_media_data(media_type, year_month):
    media_path = os.path.join(root_dir, "media", media_type, year_month)
    if not os.path.exists(media_path):
        return {}
    
    interaction_counts = defaultdict(int)
    for file_name in os.listdir(media_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(media_path, file_name)
            data = load_json_data(file_path)
            for entry in data.get('media_list_data', []):
                for string_data in entry.get('string_list_data', []):
                    interaction_counts[string_data['value']] += 1
    return interaction_counts

def aggregate_interactions():
    post_likes = {}
    story_likes = {}
    comments = {}
    
    for year_month in ["202311", "202312", "202401"]:
        post_likes.update(process_media_data("posts", year_month))
        story_likes.update(process_media_data("stories", year_month))
        comments.update(process_media_data("comments", year_month))
    
    return post_likes, story_likes, comments

def generate_top_interactions_csv():
    try:
        post_likes, story_likes, comments = aggregate_interactions()
        
        interaction_totals = defaultdict(int)
        for account, count in post_likes.items():
            interaction_totals[account] += count
        for account, count in story_likes.items():
            interaction_totals[account] += count
        for account, count in comments.items():
            interaction_totals[account] += count
        
        top_accounts = sorted(interaction_totals.items(), key=lambda x: x[1], reverse=True)[:20]
        
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
            for account, total in top_accounts:
                writer.writerow([account, post_likes.get(account, 0), story_likes.get(account, 0), comments.get(account, 0)])
        
    except Exception as e:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
        raise Exception(f"Error: {str(e)}")

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

generate_top_interactions_csv()
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

def process_post_likes():
    post_likes = defaultdict(int)
    post_likes_file = os.path.join(root_dir, "activity", "post_likes.json")
    if os.path.exists(post_likes_file):
        data = load_json_data(post_likes_file)
        for entry in data.get("post_likes", []):
            for string_data in entry.get("string_list_data", []):
                post_likes[string_data.get("value", "")] += 1
    return post_likes

def process_story_likes():
    story_likes = defaultdict(int)
    story_likes_file = os.path.join(root_dir, "story_interactions", "emoji_story_reactions.json")
    if os.path.exists(story_likes_file):
        data = load_json_data(story_likes_file)
        for entry in data.get("story_activities_emoji_quick_reactions", []):
            for string_data in entry.get("string_list_data", []):
                story_likes[string_data.get("value", "")] += 1
    return story_likes

def process_comments():
    comments = defaultdict(int)
    comments_file = os.path.join(root_dir, "activity", "comments.json")
    if os.path.exists(comments_file):
        data = load_json_data(comments_file)
        for entry in data.get("comments", []):
            for string_data in entry.get("string_list_data", []):
                comments[string_data.get("value", "")] += 1
    return comments

def aggregate_interactions():
    post_likes = process_post_likes()
    story_likes = process_story_likes()
    comments = process_comments()

    interactions = defaultdict(int)
    for account, count in post_likes.items():
        interactions[account] += count
    for account, count in story_likes.items():
        interactions[account] += count
    for account, count in comments.items():
        interactions[account] += count

    top_accounts = sorted(interactions.items(), key=lambda x: x[1], reverse=True)[:20]
    return top_accounts

def write_to_csv(top_accounts):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, total in top_accounts:
            writer.writerow({
                'User': account,
                'Post Likes': post_likes.get(account, 0),
                'Story Likes': story_likes.get(account, 0),
                'Comments': comments.get(account, 0)
            })

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    top_accounts = aggregate_interactions()
    write_to_csv(top_accounts)
except Exception as e:
    print(e)
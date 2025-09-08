import os
import json
import csv
from collections import defaultdict

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

def get_likes_data(root_directory):
    likes_file_path = os.path.join(root_directory, "your_instagram_activity", "likes", "liked_posts.json")
    if not os.path.exists(likes_file_path):
        return {}
    likes_data = load_json_file(likes_file_path)
    likes_count = defaultdict(int)
    for like in likes_data.get('likes_media_likes', []):
        for item in like.get('string_list_data', []):
            likes_count[item['value']] += 1
    return likes_count

def get_saved_data(root_directory):
    saved_file_path = os.path.join(root_directory, "your_instagram_activity", "saved", "saved_posts.json")
    if not os.path.exists(saved_file_path):
        return {}
    saved_data = load_json_file(saved_file_path)
    saved_count = defaultdict(int)
    for saved in saved_data.get('saved_saved_media', []):
        saved_count[saved.get('title', '')] += 1
    return saved_count

def aggregate_interactions(likes_count, saved_count):
    interaction_count = defaultdict(int)
    for account, count in likes_count.items():
        interaction_count[account] += count
    for account, count in saved_count.items():
        interaction_count[account] += count
    return interaction_count

def write_csv(interaction_count):
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['User', 'Post Likes', 'Story Likes and Comments'])
        for account, count in sorted(interaction_count.items(), key=lambda x: x[1], reverse=True)[:20]:
            csvwriter.writerow([account, count, 0])  # Assuming no story likes and comments data

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    likes_count = get_likes_data(root_dir)
    saved_count = get_saved_data(root_dir)
    interaction_count = aggregate_interactions(likes_count, saved_count)
    write_csv(interaction_count)

if __name__ == "__main__":
    main()
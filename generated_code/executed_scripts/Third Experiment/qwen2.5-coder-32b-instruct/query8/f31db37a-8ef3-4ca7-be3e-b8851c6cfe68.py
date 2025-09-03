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

def get_interactions_from_file(file_path, key):
    data = load_json_file(file_path)
    interactions = {}
    for item in data.get(key, []):
        for entry in item.get('string_list_data', []):
            user = entry.get('value')
            if user:
                interactions[user] = interactions.get(user, 0) + 1
    return interactions

def aggregate_interactions(root_dir):
    interactions = {}

    # Post likes
    post_likes_path = os.path.join(root_dir, 'activity', 'post_likes.json')
    if os.path.exists(post_likes_path):
        interactions.update(get_interactions_from_file(post_likes_path, 'post_likes'))

    # Story likes
    story_likes_path = os.path.join(root_dir, 'activity', 'story_likes.json')
    if os.path.exists(story_likes_path):
        interactions.update(get_interactions_from_file(story_likes_path, 'story_activities_story_likes'))

    # Comments
    comments_path = os.path.join(root_dir, 'activity', 'comments.json')
    if os.path.exists(comments_path):
        interactions.update(get_interactions_from_file(comments_path, 'story_activities_comments'))

    return interactions

def get_top_accounts(interactions, top_n=20):
    return sorted(interactions.items(), key=lambda x: x[1], reverse=True)[:top_n]

def save_to_csv(top_accounts, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['User', 'Interactions'])
            for user, count in top_accounts:
                writer.writerow([user, count])
    except IOError:
        raise IOError(f"IOError: Failed to write to the file {output_path}.")

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    interactions = aggregate_interactions(root_dir)
    top_accounts = get_top_accounts(interactions)

    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    save_to_csv(top_accounts, output_path)

if __name__ == "__main__":
    main()
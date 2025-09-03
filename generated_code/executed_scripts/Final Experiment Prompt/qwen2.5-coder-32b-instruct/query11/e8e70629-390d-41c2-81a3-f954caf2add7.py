import os
import json
import csv

# Variable referring to the file input
root_dir = "root_dir"

def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

def get_viewed_accounts(data):
    viewed_accounts = set()
    if 'impressions_history_posts_seen' in data:
        for entry in data['impressions_history_posts_seen']:
            if 'string_map_data' in entry and 'Author' in entry['string_map_data']:
                author = entry['string_map_data']['Author']['value']
                viewed_accounts.add(author)
    return viewed_accounts

def get_liked_accounts(data):
    liked_accounts = set()
    if 'likes_media_likes' in data:
        for entry in data['likes_media_likes']:
            if 'title' in entry:
                liked_accounts.add(entry['title'])
    return liked_accounts

def main():
    # Define file paths
    posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")

    # Initialize sets to store viewed and liked accounts
    viewed_accounts = set()
    liked_accounts = set()

    # Read and process posts_viewed.json
    try:
        if os.path.exists(posts_viewed_path):
            posts_viewed_data = read_json_file(posts_viewed_path)
            viewed_accounts = get_viewed_accounts(posts_viewed_data)
        else:
            print(f"Warning: The file {posts_viewed_path} does not exist. Skipping this file.")
    except (FileNotFoundError, ValueError) as e:
        print(e)

    # Read and process liked_posts.json
    try:
        if os.path.exists(liked_posts_path):
            liked_posts_data = read_json_file(liked_posts_path)
            liked_accounts = get_liked_accounts(liked_posts_data)
        else:
            print(f"Warning: The file {liked_posts_path} does not exist. Skipping this file.")
    except (FileNotFoundError, ValueError) as e:
        print(e)

    # Calculate accounts viewed but not liked
    result_accounts = viewed_accounts - liked_accounts

    # Define the output CSV file path
    output_csv_path = 'query_responses/results.csv'

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

    # Write the result to a CSV file
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Account'])
        for account in result_accounts:
            csvwriter.writerow([account])

if __name__ == "__main__":
    main()
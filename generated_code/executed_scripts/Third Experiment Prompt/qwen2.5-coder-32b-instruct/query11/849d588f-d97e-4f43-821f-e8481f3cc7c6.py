import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Function to read JSON file and return its content
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to get the list of accounts from posts_viewed.json
def get_viewed_accounts(root_dir):
    viewed_accounts = set()
    file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    if os.path.exists(file_path):
        data = read_json_file(file_path)
        if "impressions_history_posts_seen" in data:
            for entry in data["impressions_history_posts_seen"]:
                if "string_map_data" in entry and "Author" in entry["string_map_data"]:
                    viewed_accounts.add(entry["string_map_data"]["Author"]["value"])
    return viewed_accounts

# Function to get the list of accounts from liked_posts.json
def get_liked_accounts(root_dir):
    liked_accounts = set()
    file_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
    if os.path.exists(file_path):
        data = read_json_file(file_path)
        if "likes_media_likes" in data:
            for entry in data["likes_media_likes"]:
                if "string_list_data" in entry:
                    for item in entry["string_list_data"]:
                        if "value" in item:
                            liked_accounts.add(item["value"])
    return liked_accounts

# Main function to find accounts viewed but not liked
def find_viewed_but_not_liked_accounts(root_dir):
    try:
        viewed_accounts = get_viewed_accounts(root_dir)
        liked_accounts = get_liked_accounts(root_dir)
        result_accounts = viewed_accounts - liked_accounts

        # Write the result to a CSV file
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for account in result_accounts:
                writer.writerow([account])
    except Exception as e:
        # If any error occurs, write only the column headers
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])

# Execute the main function
find_viewed_but_not_liked_accounts(root_dir)
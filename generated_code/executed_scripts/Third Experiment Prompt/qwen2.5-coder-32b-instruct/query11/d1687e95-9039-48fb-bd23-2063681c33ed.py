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

# Function to extract viewed accounts from posts_viewed.json
def get_viewed_accounts(root_dir):
    viewed_accounts = set()
    file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    if os.path.exists(file_path):
        data = read_json_file(file_path)
        for entry in data.get("impressions_history_posts_seen", []):
            string_map_data = entry.get("string_map_data", {})
            author = string_map_data.get("Author", {}).get("value")
            if author:
                viewed_accounts.add(author)
    return viewed_accounts

# Function to extract liked accounts from liked_posts.json
def get_liked_accounts(root_dir):
    liked_accounts = set()
    file_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
    if os.path.exists(file_path):
        data = read_json_file(file_path)
        for entry in data.get("likes_media_likes", []):
            string_list_data = entry.get("string_list_data", [])
            for item in string_list_data:
                value = item.get("value")
                if value:
                    liked_accounts.add(value)
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

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Execute the main function
find_viewed_but_not_liked_accounts(root_dir)
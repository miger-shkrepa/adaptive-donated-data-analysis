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

# Function to get the list of viewed accounts from posts_viewed.json
def get_viewed_accounts(root_dir):
    viewed_accounts = set()
    posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    
    if os.path.exists(posts_viewed_path):
        posts_viewed_data = read_json_file(posts_viewed_path)
        for post in posts_viewed_data.get("impressions_history_posts_seen", []):
            author = post.get("string_map_data", {}).get("Author", {}).get("value")
            if author:
                viewed_accounts.add(author)
    
    return viewed_accounts

# Function to get the list of liked accounts from liked_posts.json
def get_liked_accounts(root_dir):
    liked_accounts = set()
    liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
    
    if os.path.exists(liked_posts_path):
        liked_posts_data = read_json_file(liked_posts_path)
        for liked_post in liked_posts_data.get("likes_media_likes", []):
            for item in liked_post.get("string_list_data", []):
                author = item.get("value")
                if author:
                    liked_accounts.add(author)
    
    return liked_accounts

# Main function to find accounts viewed but not liked
def find_viewed_but_not_liked_accounts(root_dir):
    try:
        viewed_accounts = get_viewed_accounts(root_dir)
        liked_accounts = get_liked_accounts(root_dir)
        
        # Find accounts that are viewed but not liked
        viewed_but_not_liked_accounts = viewed_accounts - liked_accounts
        
        # Write the result to a CSV file
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for account in viewed_but_not_liked_accounts:
                writer.writerow([account])
    
    except Exception as e:
        # If any error occurs, write only the column headers to the CSV file
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])

# Ensure the output directory exists
os.makedirs('query_responses', exist_ok=True)

# Execute the main function
find_viewed_but_not_liked_accounts(root_dir)
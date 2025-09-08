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
    posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    
    if not os.path.exists(posts_viewed_path):
        return viewed_accounts
    
    try:
        data = read_json_file(posts_viewed_path)
        for entry in data.get("impressions_history_posts_seen", []):
            author = entry.get("string_map_data", {}).get("Author", {}).get("value")
            if author:
                viewed_accounts.add(author)
    except Exception as e:
        print(f"Error processing {posts_viewed_path}: {e}")
    
    return viewed_accounts

# Function to extract liked accounts from liked_posts.json
def get_liked_accounts(root_dir):
    liked_accounts = set()
    liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
    
    if not os.path.exists(liked_posts_path):
        return liked_accounts
    
    try:
        data = read_json_file(liked_posts_path)
        for entry in data.get("likes_media_likes", []):
            for item in entry.get("string_list_data", []):
                author = item.get("value")
                if author:
                    liked_accounts.add(author)
    except Exception as e:
        print(f"Error processing {liked_posts_path}: {e}")
    
    return liked_accounts

# Main function to find accounts viewed but not liked
def find_viewed_but_not_liked_accounts(root_dir):
    viewed_accounts = get_viewed_accounts(root_dir)
    liked_accounts = get_liked_accounts(root_dir)
    
    # Find the difference
    viewed_but_not_liked_accounts = viewed_accounts - liked_accounts
    
    # Write the result to a CSV file
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Account'])
        for account in viewed_but_not_liked_accounts:
            writer.writerow([account])

# Execute the main function
try:
    find_viewed_but_not_liked_accounts(root_dir)
except Exception as e:
    print(f"Error: {e}")
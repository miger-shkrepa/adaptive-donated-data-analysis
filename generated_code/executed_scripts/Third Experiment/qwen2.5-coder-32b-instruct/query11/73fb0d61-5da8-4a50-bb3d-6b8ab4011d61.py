import os
import csv
import json

root_dir = "root_dir"

def find_unliked_accounts(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Define paths for the required files
        posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        
        # Initialize sets to store viewed and liked accounts
        viewed_accounts = set()
        liked_accounts = set()
        
        # Load and process posts_viewed.json
        if os.path.exists(posts_viewed_path):
            with open(posts_viewed_path, 'r', encoding='utf-8') as file:
                posts_viewed_data = json.load(file)
                for entry in posts_viewed_data.get("impressions_history_posts_seen", []):
                    author = entry.get("string_map_data", {}).get("Author", {}).get("value")
                    if author:
                        viewed_accounts.add(author)
        else:
            print("Warning: posts_viewed.json not found. Continuing with available data.")
        
        # Load and process liked_posts.json
        if os.path.exists(liked_posts_path):
            with open(liked_posts_path, 'r', encoding='utf-8') as file:
                liked_posts_data = json.load(file)
                for entry in liked_posts_data.get("likes_media_likes", []):
                    for item in entry.get("string_list_data", []):
                        author = item.get("value")
                        if author:
                            liked_accounts.add(author)
        else:
            print("Warning: liked_posts.json not found. Continuing with available data.")
        
        # Find accounts that were viewed but not liked
        unliked_accounts = viewed_accounts - liked_accounts
        
        # Write the result to a CSV file
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for account in unliked_accounts:
                writer.writerow([account])
    
    except FileNotFoundError as e:
        # Create an empty CSV file with only the column headers if a required file is missing
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
        print(e)
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")

# Call the function to execute the script
find_unliked_accounts(root_dir)
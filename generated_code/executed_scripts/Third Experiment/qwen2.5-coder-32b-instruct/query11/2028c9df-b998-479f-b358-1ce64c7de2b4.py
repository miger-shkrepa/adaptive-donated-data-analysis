import os
import csv
import json

root_dir = "root_dir"

def find_viewed_posts_accounts(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Define paths for the required files
        posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        story_likes_path = os.path.join(root_dir, "connections", "followers_and_following", "recently_unfollowed_accounts.json")
        
        # Check if the posts_viewed.json file exists
        if not os.path.exists(posts_viewed_path):
            raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")
        
        # Check if the story_likes.json file exists
        if not os.path.exists(story_likes_path):
            raise FileNotFoundError("FileNotFoundError: The recently_unfollowed_accounts.json file does not exist.")
        
        # Load the posts_viewed.json file
        with open(posts_viewed_path, 'r') as file:
            posts_viewed_data = json.load(file)
        
        # Load the story_likes.json file
        with open(story_likes_path, 'r') as file:
            story_likes_data = json.load(file)
        
        # Extract viewed posts accounts
        viewed_posts_accounts = set()
        for entry in posts_viewed_data.get("impressions_history_posts_seen", []):
            author = entry.get("string_map_data", {}).get("Author", {}).get("value")
            if author:
                viewed_posts_accounts.add(author)
        
        # Extract liked stories accounts
        liked_stories_accounts = set()
        for entry in story_likes_data.get("story_activities_story_likes", []):
            for item in entry.get("string_list_data", []):
                value = item.get("value")
                if value:
                    liked_stories_accounts.add(value)
        
        # Find accounts that have been viewed but not liked
        result_accounts = viewed_posts_accounts - liked_stories_accounts
        
        # Write the result to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for account in result_accounts:
                writer.writerow([account])
    
    except FileNotFoundError as e:
        # Create a CSV file with only the column headers if a required file is missing
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
        print(e)
    except Exception as e:
        print(f"Error: An unexpected error occurred - {str(e)}")

# Call the function to execute the query
find_viewed_posts_accounts(root_dir)
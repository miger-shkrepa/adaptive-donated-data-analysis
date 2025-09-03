import os
import csv

root_dir = "root_dir"

def find_accounts_viewed_but_not_liked(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Initialize a set to store accounts viewed
        accounts_viewed = set()
        
        # Initialize a set to store accounts liked
        accounts_liked = set()
        
        # Path to posts_viewed.json
        posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        
        # Path to story_likes.json
        story_likes_path = os.path.join(root_dir, "story_interactions", "story_likes.json")
        
        # Check if posts_viewed.json exists and read data
        if os.path.exists(posts_viewed_path):
            with open(posts_viewed_path, 'r') as file:
                import json
                data = json.load(file)
                for entry in data.get("impressions_history_posts_seen", []):
                    author = entry.get("string_map_data", {}).get("Author", {}).get("value")
                    if author:
                        accounts_viewed.add(author)
        else:
            print("Warning: posts_viewed.json does not exist. Skipping account viewed data.")
        
        # Check if story_likes.json exists and read data
        if os.path.exists(story_likes_path):
            with open(story_likes_path, 'r') as file:
                import json
                data = json.load(file)
                for entry in data.get("story_activities_story_likes", []):
                    for item in entry.get("string_list_data", []):
                        href = item.get("href")
                        if href:
                            # Assuming the account name is part of the href, we extract it
                            # This is a simplification and might need adjustment based on actual data format
                            account_name = href.split('/')[-1]
                            accounts_liked.add(account_name)
        else:
            print("Warning: story_likes.json does not exist. Skipping account liked data.")
        
        # Find accounts viewed but not liked
        accounts_viewed_but_not_liked = accounts_viewed - accounts_liked
        
        # Write the result to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for account in accounts_viewed_but_not_liked:
                writer.writerow([account])
    
    except Exception as e:
        print(f"Error: {str(e)}")
        # Create an empty CSV file with only the column headers if an error occurs
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])

# Call the function
find_accounts_viewed_but_not_liked(root_dir)
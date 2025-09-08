import os
import csv

root_dir = "root_dir"

def find_viewed_but_not_liked_accounts(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Initialize a set to store viewed accounts
        viewed_accounts = set()
        
        # Initialize a set to store liked accounts
        liked_accounts = set()
        
        # Path to the messages directory
        messages_dir = os.path.join(root_dir, "messages", "inbox")
        
        # Check if the messages directory exists
        if os.path.exists(messages_dir):
            # Iterate through each user's message directory
            for user_dir in os.listdir(messages_dir):
                user_messages_dir = os.path.join(messages_dir, user_dir)
                
                # Check if the user's message directory is a directory
                if os.path.isdir(user_messages_dir):
                    # Iterate through each message file
                    for message_file in os.listdir(user_messages_dir):
                        message_file_path = os.path.join(user_messages_dir, message_file)
                        
                        # Check if the message file is a JSON file
                        if message_file.endswith(".json"):
                            with open(message_file_path, 'r', encoding='utf-8') as file:
                                import json
                                data = json.load(file)
                                
                                # Extract viewed accounts
                                for message in data.get("messages", []):
                                    viewed_accounts.add(message.get("sender_name", ""))
                                
                                # Extract liked accounts from liked_posts.json
                                liked_posts_path = os.path.join(root_dir, "likes", "liked_posts.json")
                                if os.path.exists(liked_posts_path):
                                    with open(liked_posts_path, 'r', encoding='utf-8') as liked_file:
                                        liked_data = json.load(liked_file)
                                        for liked_post in liked_data.get("likes_media_likes", []):
                                            for string_data in liked_post.get("string_list_data", []):
                                                liked_accounts.add(string_data.get("value", ""))
        
        # Find accounts that were viewed but not liked
        result_accounts = viewed_accounts - liked_accounts
        
        # Write the result to a CSV file
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account"])
            for account in result_accounts:
                writer.writerow([account])
    
    except Exception as e:
        # Write an empty CSV file with only the column headers if an error occurs
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account"])
        print(f"Error: {str(e)}")

# Call the function to execute the query
find_viewed_but_not_liked_accounts(root_dir)
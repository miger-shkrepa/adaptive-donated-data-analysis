import os
import csv
import json

root_dir = "root_dir"

def find_viewed_but_not_liked_accounts(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Initialize a set to store accounts viewed but not liked
        viewed_accounts = set()
        liked_accounts = set()
        
        # Traverse the messages directory to find viewed accounts
        messages_dir = os.path.join(root_dir, "messages", "inbox")
        if os.path.exists(messages_dir):
            for username in os.listdir(messages_dir):
                user_dir = os.path.join(messages_dir, username)
                if os.path.isdir(user_dir):
                    for message_file in os.listdir(user_dir):
                        if message_file.endswith(".json"):
                            message_path = os.path.join(user_dir, message_file)
                            with open(message_path, 'r', encoding='utf-8') as file:
                                messages_data = json.load(file)
                                for message in messages_data.get('messages', []):
                                    if 'sender_name' in message:
                                        viewed_accounts.add(message['sender_name'])
        
        # Traverse the likes directory to find liked accounts
        likes_dir = os.path.join(root_dir, "likes", "liked_posts.json")
        if os.path.exists(likes_dir):
            with open(likes_dir, 'r', encoding='utf-8') as file:
                likes_data = json.load(file)
                for like in likes_data.get('likes_media_likes', []):
                    for string_data in like.get('string_list_data', []):
                        if 'value' in string_data:
                            liked_accounts.add(string_data['value'])
        
        # Find accounts that were viewed but not liked
        result_accounts = viewed_accounts - liked_accounts
        
        # Write the result to a CSV file
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for account in result_accounts:
                writer.writerow([account])
    
    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")

# Call the function to execute the query
find_viewed_but_not_liked_accounts(root_dir)
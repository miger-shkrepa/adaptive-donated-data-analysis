import os
import json
import csv

root_dir = "root_dir"

def get_account_info(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize sets to store viewed and liked accounts
        viewed_accounts = set()
        liked_accounts = set()

        # Iterate over all files in the directory
        for dir_path, dir_names, file_names in os.walk(root_dir):
            for file_name in file_names:
                # Check if file is 'posts_viewed.json'
                if file_name == 'posts_viewed.json':
                    file_path = os.path.join(dir_path, file_name)
                    try:
                        with open(file_path, 'r') as file:
                            data = json.load(file)
                            for post in data['impressions_history_posts_seen']:
                                viewed_accounts.add(post['string_map_data']['Author']['value'])
                    except json.JSONDecodeError:
                        raise ValueError("Error: Failed to parse JSON in 'posts_viewed.json'.")

                # Check if file is 'in-app_message.json'
                elif file_name == 'in-app_message.json':
                    file_path = os.path.join(dir_path, file_name)
                    try:
                        with open(file_path, 'r') as file:
                            data = json.load(file)
                            for message in data['impressions_history_app_message']:
                                if message['string_map_data']['Click type']['value'] == 'Like':
                                    liked_accounts.add(message['string_map_data']['In-app message name']['value'])
                    except json.JSONDecodeError:
                        raise ValueError("Error: Failed to parse JSON in 'in-app_message.json'.")

        # Find accounts that have been viewed but not liked
        not_liked_accounts = viewed_accounts - liked_accounts

        return not_liked_accounts

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def write_to_csv(accounts):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Account'])
            for account in accounts:
                writer.writerow([account])
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def main():
    try:
        accounts = get_account_info(root_dir)
        write_to_csv(accounts)
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Account'])
        print(e)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
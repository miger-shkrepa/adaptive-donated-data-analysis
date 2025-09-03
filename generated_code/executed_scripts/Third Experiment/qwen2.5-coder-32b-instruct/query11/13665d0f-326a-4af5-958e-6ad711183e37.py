import os
import csv
import json

root_dir = "root_dir"

def get_viewed_accounts(root_directory):
    viewed_accounts = set()
    posts_viewed_path = os.path.join(root_directory, "ads_information", "ads_and_topics", "posts_viewed.json")
    
    if not os.path.exists(root_directory):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.exists(posts_viewed_path):
        raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")
    
    try:
        with open(posts_viewed_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for entry in data.get('impressions_history_posts_seen', []):
                author = entry.get('string_map_data', {}).get('Author', {}).get('value')
                if author:
                    viewed_accounts.add(author)
    except json.JSONDecodeError:
        raise ValueError("ValueError: The posts_viewed.json file is not a valid JSON file.")
    
    return viewed_accounts

def main():
    try:
        viewed_accounts = get_viewed_accounts(root_dir)
        
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for account in viewed_accounts:
                writer.writerow([account])
    except Exception as e:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])

if __name__ == "__main__":
    main()
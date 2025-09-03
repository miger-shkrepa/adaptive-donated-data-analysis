import os
import csv
import json

root_dir = "root_dir"

def get_viewed_posts_accounts(root_directory):
    posts_viewed_path = os.path.join(root_directory, "ads_information", "ads_and_topics", "posts_viewed.json")
    
    if not os.path.exists(root_directory):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.exists(posts_viewed_path):
        raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")
    
    with open(posts_viewed_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            raise ValueError("ValueError: The posts_viewed.json file is not a valid JSON file.")
    
    accounts_viewed = set()
    
    if 'impressions_history_posts_seen' in data:
        for entry in data['impressions_history_posts_seen']:
            if 'string_map_data' in entry and 'Author' in entry['string_map_data']:
                author = entry['string_map_data']['Author'].get('value')
                if author:
                    accounts_viewed.add(author)
    
    return accounts_viewed

def main():
    try:
        accounts_viewed = get_viewed_posts_accounts(root_dir)
        
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for account in accounts_viewed:
                writer.writerow([account])
    
    except (FileNotFoundError, ValueError) as e:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])

if __name__ == "__main__":
    main()
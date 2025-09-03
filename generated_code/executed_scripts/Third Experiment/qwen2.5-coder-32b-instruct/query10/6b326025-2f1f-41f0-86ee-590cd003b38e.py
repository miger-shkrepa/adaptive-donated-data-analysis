import os
import csv
import json

root_dir = "root_dir"

def get_account_views(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")
    
    account_views = {}
    if 'story_activities_story_likes' in data:
        for entry in data['story_activities_story_likes']:
            account = entry.get('title', 'Unknown')
            views = len(entry.get('string_list_data', []))
            account_views[account] = account_views.get(account, 0) + views
    
    if 'story_activities_quizzes' in data:
        for entry in data['story_activities_quizzes']:
            account = entry.get('title', 'Unknown')
            views = len(entry.get('string_list_data', []))
            account_views[account] = account_views.get(account, 0) + views
    
    return account_views

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        story_likes_path = os.path.join(root_dir, 'story_likes.json')
        quizzes_path = os.path.join(root_dir, 'quizzes.json')
        
        account_views = {}
        
        if os.path.exists(story_likes_path):
            account_views.update(get_account_views(story_likes_path))
        
        if os.path.exists(quizzes_path):
            account_views.update(get_account_views(quizzes_path))
        
        # Assuming video views are not available in the provided structure
        video_views = {account: 0 for account in account_views}
        
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account', 'Post Views', 'Video Views'])
            for account in account_views:
                writer.writerow([account, account_views[account], video_views[account]])
    
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
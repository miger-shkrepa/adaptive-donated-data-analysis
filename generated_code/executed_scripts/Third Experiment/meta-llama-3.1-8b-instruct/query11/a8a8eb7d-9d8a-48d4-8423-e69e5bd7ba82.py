import csv
import os

def get_account_names(root_dir):
    account_names = set()
    for dir_path, dir_names, file_names in os.walk(root_dir):
        for file_name in file_names:
            if file_name.endswith('.json'):
                file_path = os.path.join(dir_path, file_name)
                with open(file_path, 'r') as file:
                    data = file.read()
                    if 'likes_media_likes' in data:
                        account_names.add(file_path.split(os.sep)[-2])
                    elif 'impressions_history_posts_seen' in data:
                        account_names.add(file_path.split(os.sep)[-2])
    return account_names

def get_liked_posts(root_dir):
    liked_posts = set()
    for dir_path, dir_names, file_names in os.walk(root_dir):
        for file_name in file_names:
            if file_name.endswith('.json'):
                file_path = os.path.join(dir_path, file_name)
                with open(file_path, 'r') as file:
                    data = file.read()
                    if 'likes_media_likes' in data:
                        for post in eval(data)['likes_media_likes']:
                            liked_posts.add(post['title'])
    return liked_posts

def get_viewed_posts(root_dir):
    viewed_posts = set()
    for dir_path, dir_names, file_names in os.walk(root_dir):
        for file_name in file_names:
            if file_name.endswith('.json'):
                file_path = os.path.join(dir_path, file_name)
                with open(file_path, 'r') as file:
                    data = file.read()
                    if 'impressions_history_posts_seen' in data:
                        for post in eval(data)['impressions_history_posts_seen']:
                            viewed_posts.add(post['string_map_data']['Author']['value'])
    return viewed_posts

def main():
    root_dir = "root_dir"
    try:
        os.listdir(root_dir)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    account_names = get_account_names(root_dir)
    liked_posts = get_liked_posts(root_dir)
    viewed_posts = get_viewed_posts(root_dir)
    
    with open('query_responses/results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Account'])
        for account in account_names:
            if account not in liked_posts and account in viewed_posts:
                writer.writerow([account])

if __name__ == "__main__":
    main()
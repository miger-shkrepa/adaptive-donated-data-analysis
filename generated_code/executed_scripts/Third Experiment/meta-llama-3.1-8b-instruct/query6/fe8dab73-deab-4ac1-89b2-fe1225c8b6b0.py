import csv
import os
import datetime

def get_user_changes(root_dir):
    user_changes = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.json'):
                with open(os.path.join(root, file), 'r') as f:
                    data = eval(f.read())
                    if 'your_instagram_activity' in data:
                        likes_data = data['your_instagram_activity']['likes']
                        saved_data = data['your_instagram_activity']['saved']
                        if 'liked_posts.json' in likes_data and 'saved_posts.json' in saved_data:
                            likes_media_likes = likes_data['liked_posts.json']['structure']['likes_media_likes']
                            saved_saved_media = saved_data['saved_posts.json']['structure']['saved_saved_media']
                            for like in likes_media_likes:
                                for saved in saved_saved_media:
                                    if like['title'] == saved['title']:
                                        user_changes.append({
                                            'Changed': like['title'],
                                            'New Value': saved['string_map_data']['Saved on']['href'],
                                            'Change Date': datetime.datetime.now().strftime('%Y-%m-%d')
                                        })
    return user_changes

def main():
    try:
        root_dir = "root_dir"
        user_changes = get_user_changes(root_dir)
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Changed', 'New Value', 'Change Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for change in user_changes:
                writer.writerow(change)
    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except Exception as e:
        raise ValueError("ValueError: An error occurred while processing the data.")

if __name__ == "__main__":
    main()
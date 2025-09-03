import os
import json
import csv

root_dir = "root_dir"

def get_views_and_accounts(root_dir):
    views = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == "posts_1.json":
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        for post in data:
                            if 'media' in post:
                                for media in post['media']:
                                    if 'uri' in media:
                                        account = media['uri'].split('/')[3]
                                        if account not in views:
                                            views[account] = {'post_views': 0, 'video_views': 0}
                                        views[account]['post_views'] += 1
                except FileNotFoundError:
                    raise FileNotFoundError("Error: The file {} does not exist.".format(file_path))
                except json.JSONDecodeError:
                    raise ValueError("Error: The file {} is not a valid JSON file.".format(file_path))
            elif filename == "stories.json":
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        for story in data['ig_stories']:
                            if 'uri' in story:
                                account = story['uri'].split('/')[3]
                                if account not in views:
                                    views[account] = {'post_views': 0, 'video_views': 0}
                                if 'video_metadata' in story['media_metadata']:
                                    views[account]['video_views'] += 1
                                else:
                                    views[account]['post_views'] += 1
                except FileNotFoundError:
                    raise FileNotFoundError("Error: The file {} does not exist.".format(file_path))
                except json.JSONDecodeError:
                    raise ValueError("Error: The file {} is not a valid JSON file.".format(file_path))
    return views

def save_to_csv(views):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, view_counts in views.items():
            writer.writerow({'Account': account, 'Post Views': view_counts['post_views'], 'Video Views': view_counts['video_views']})

def main():
    try:
        views = get_views_and_accounts(root_dir)
        save_to_csv(views)
    except FileNotFoundError as e:
        print(e)
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Account', 'Post Views', 'Video Views']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    except ValueError as e:
        print(e)
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Account', 'Post Views', 'Video Views']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

if __name__ == "__main__":
    main()
import csv
import os

def get_post_views(root_dir):
    post_views = 0
    for filename in os.listdir(root_dir):
        if filename.startswith('posts_viewed'):
            try:
                with open(os.path.join(root_dir, filename), 'r') as file:
                    data = file.read()
                    post_views += len(data.split('"Time": {"timestamp": ')[1:])
            except FileNotFoundError:
                raise FileNotFoundError("FileNotFoundError: The file {} does not exist.".format(filename))
            except ValueError:
                raise ValueError("ValueError: The file {} is not in the correct format.".format(filename))
    return post_views

def get_video_views(root_dir):
    video_views = 0
    for filename in os.listdir(root_dir):
        if filename.startswith('videos_watched'):
            try:
                with open(os.path.join(root_dir, filename), 'r') as file:
                    data = file.read()
                    video_views += len(data.split('"Time": {"timestamp": ')[1:])
            except FileNotFoundError:
                raise FileNotFoundError("FileNotFoundError: The file {} does not exist.".format(filename))
            except ValueError:
                raise ValueError("ValueError: The file {} is not in the correct format.".format(filename))
    return video_views

def get_account_names(root_dir):
    account_names = set()
    for filename in os.listdir(root_dir):
        if filename.startswith('posts_viewed') or filename.startswith('videos_watched'):
            try:
                with open(os.path.join(root_dir, filename), 'r') as file:
                    data = file.read()
                    for line in data.splitlines():
                        if '"Author": {"value": "' in line:
                            account_names.add(line.split('"value": "')[1].split('"')[0])
            except FileNotFoundError:
                raise FileNotFoundError("FileNotFoundError: The file {} does not exist.".format(filename))
            except ValueError:
                raise ValueError("ValueError: The file {} is not in the correct format.".format(filename))
    return account_names

def main():
    root_dir = "root_dir"
    try:
        post_views = get_post_views(root_dir)
        video_views = get_video_views(root_dir)
        account_names = get_account_names(root_dir)
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account', 'Post Views', 'Video Views'])
            for account in account_names:
                writer.writerow([account, post_views, video_views])
    except FileNotFoundError as e:
        print(e)
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account', 'Post Views', 'Video Views'])
    except ValueError as e:
        print(e)
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account', 'Post Views', 'Video Views'])

if __name__ == "__main__":
    main()
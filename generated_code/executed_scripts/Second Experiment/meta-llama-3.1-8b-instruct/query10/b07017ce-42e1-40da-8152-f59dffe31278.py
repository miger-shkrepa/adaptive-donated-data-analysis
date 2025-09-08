import csv
import os

def get_post_views(root_dir):
    post_views = 0
    for filename in os.listdir(root_dir):
        if filename.startswith('posts_viewed'):
            try:
                with open(os.path.join(root_dir, filename), 'r') as file:
                    data = file.read()
                    if data:
                        post_views += len(data.split('Author'))
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    return post_views

def get_video_views(root_dir):
    video_views = 0
    for filename in os.listdir(root_dir):
        if filename.startswith('videos_watched'):
            try:
                with open(os.path.join(root_dir, filename), 'r') as file:
                    data = file.read()
                    if data:
                        video_views += len(data.split('Author'))
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    return video_views

def get_account_names(root_dir):
    account_names = set()
    for filename in os.listdir(root_dir):
        if filename.startswith('ads_viewed'):
            try:
                with open(os.path.join(root_dir, filename), 'r') as file:
                    data = file.read()
                    if data:
                        for line in data.split('\n'):
                            if 'Author' in line:
                                account_names.add(line.split('Author')[1].split(':')[0])
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    return account_names

def main():
    root_dir = "root_dir"
    try:
        os.listdir(root_dir)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    post_views = get_post_views(root_dir)
    video_views = get_video_views(root_dir)
    account_names = get_account_names(root_dir)

    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account", "Post Views", "Video Views"])
        for account in account_names:
            writer.writerow([account, post_views, video_views])

if __name__ == "__main__":
    main()
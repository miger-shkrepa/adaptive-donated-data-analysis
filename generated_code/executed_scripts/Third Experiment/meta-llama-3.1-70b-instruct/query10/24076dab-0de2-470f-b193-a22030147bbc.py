import os
import csv

root_dir = "root_dir"

def get_account_views(root_dir):
    account_views = {}
    try:
        for filename in os.listdir(os.path.join(root_dir, "media", "posts")):
            if filename.endswith(".srt") or filename.endswith(".mp4"):
                account = os.path.basename(filename).split("_")[0]
                if account not in account_views:
                    account_views[account] = {"post_views": 0, "video_views": 0}
                if filename.endswith(".srt"):
                    account_views[account]["post_views"] += 1
                elif filename.endswith(".mp4"):
                    account_views[account]["video_views"] += 1
    except FileNotFoundError:
        raise FileNotFoundError("Error: The media/posts directory does not exist.")
    return account_views

def write_csv(account_views):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ["Account", "Post Views", "Video Views"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, views in account_views.items():
            writer.writerow({"Account": account, "Post Views": views["post_views"], "Video Views": views["video_views"]})

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")
        account_views = get_account_views(root_dir)
        write_csv(account_views)
    except Exception as e:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ["Account", "Post Views", "Video Views"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        raise Exception(str(e))

if __name__ == "__main__":
    main()
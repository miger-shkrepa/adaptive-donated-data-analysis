import os
import json
import csv

root_dir = "root_dir"

def get_account_views(root_dir):
    account_views = {}
    try:
        ads_info_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
        if not os.path.exists(ads_info_dir):
            raise FileNotFoundError("FileNotFoundError: The ads_and_topics directory does not exist.")

        posts_viewed_file = os.path.join(ads_info_dir, "posts_viewed.json")
        if not os.path.exists(posts_viewed_file):
            posts_viewed = 0
        else:
            with open(posts_viewed_file, 'r') as f:
                posts_viewed_data = json.load(f)
                posts_viewed = len(posts_viewed_data["impressions_history_posts_seen"])

        videos_watched_file = os.path.join(ads_info_dir, "videos_watched.json")
        if not os.path.exists(videos_watched_file):
            videos_watched = 0
        else:
            with open(videos_watched_file, 'r') as f:
                videos_watched_data = json.load(f)
                videos_watched = len(videos_watched_data["impressions_history_videos_watched"])

        your_instagram_activity_dir = os.path.join(root_dir, "your_instagram_activity")
        if not os.path.exists(your_instagram_activity_dir):
            raise FileNotFoundError("FileNotFoundError: The your_instagram_activity directory does not exist.")

        comments_dir = os.path.join(your_instagram_activity_dir, "comments")
        if not os.path.exists(comments_dir):
            comments = 0
        else:
            reels_comments_file = os.path.join(comments_dir, "reels_comments.json")
            if not os.path.exists(reels_comments_file):
                comments = 0
            else:
                with open(reels_comments_file, 'r') as f:
                    comments_data = json.load(f)
                    comments = len(comments_data["comments_reels_comments"])

        likes_dir = os.path.join(your_instagram_activity_dir, "likes")
        if not os.path.exists(likes_dir):
            likes = 0
        else:
            liked_posts_file = os.path.join(likes_dir, "liked_posts.json")
            if not os.path.exists(liked_posts_file):
                likes = 0
            else:
                with open(liked_posts_file, 'r') as f:
                    likes_data = json.load(f)
                    likes = len(likes_data["likes_media_likes"])

        account_views["Account"] = "User"
        account_views["Post Views"] = posts_viewed
        account_views["Video Views"] = videos_watched

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")

    return account_views

def save_to_csv(account_views):
    csv_file = 'query_responses/results.csv'
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Account", "Post Views", "Video Views"])
        writer.writeheader()
        writer.writerow(account_views)

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        account_views = get_account_views(root_dir)
        save_to_csv(account_views)
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["Account", "Post Views", "Video Views"])
            writer.writeheader()
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
import os
import json
import csv

root_dir = "root_dir"

def get_account_views(root_dir):
    account_views = {}
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Check if the 'ads_information' directory exists
        ads_info_dir = os.path.join(root_dir, 'ads_information')
        if not os.path.exists(ads_info_dir):
            return account_views

        # Check if the 'ads_and_topics' directory exists
        ads_and_topics_dir = os.path.join(ads_info_dir, 'ads_and_topics')
        if not os.path.exists(ads_and_topics_dir):
            return account_views

        # Check if the 'posts_viewed.json' file exists
        posts_viewed_file = os.path.join(ads_and_topics_dir, 'posts_viewed.json')
        if os.path.exists(posts_viewed_file):
            with open(posts_viewed_file, 'r') as file:
                posts_viewed_data = json.load(file)
                for post in posts_viewed_data['impressions_history_posts_seen']:
                    author = post['string_map_data']['Author']['value']
                    if author not in account_views:
                        account_views[author] = {'post_views': 1, 'video_views': 0}
                    else:
                        account_views[author]['post_views'] += 1

        # Check if the 'videos_watched.json' file exists
        videos_watched_file = os.path.join(ads_and_topics_dir, 'videos_watched.json')
        if os.path.exists(videos_watched_file):
            with open(videos_watched_file, 'r') as file:
                videos_watched_data = json.load(file)
                for video in videos_watched_data['impressions_history_videos_watched']:
                    # Since there is no author information in the 'videos_watched.json' file,
                    # we will assume that the video views are from the same accounts as the post views
                    for author in account_views:
                        if 'video_views' not in account_views[author]:
                            account_views[author]['video_views'] = 1
                        else:
                            account_views[author]['video_views'] += 1

        return account_views

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(account_views):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Account', 'Post Views', 'Video Views'])
            for author, views in account_views.items():
                writer.writerow([author, views.get('post_views', 0), views.get('video_views', 0)])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    account_views = get_account_views(root_dir)
    if not account_views:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Account', 'Post Views', 'Video Views'])
    else:
        save_to_csv(account_views)

if __name__ == "__main__":
    main()
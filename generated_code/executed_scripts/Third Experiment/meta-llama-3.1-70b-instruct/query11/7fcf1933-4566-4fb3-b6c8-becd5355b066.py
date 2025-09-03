import os
import json
import csv

root_dir = "root_dir"

def get_viewed_but_not_liked_accounts(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize set to store liked accounts
        liked_accounts = set()

        # Initialize set to store viewed accounts
        viewed_accounts = set()

        # Check if 'your_instagram_activity' directory exists
        activity_dir = os.path.join(root_dir, 'your_instagram_activity')
        if os.path.exists(activity_dir):
            # Check if 'likes' directory exists
            likes_dir = os.path.join(activity_dir, 'likes')
            if os.path.exists(likes_dir):
                # Check if 'liked_posts.json' file exists
                liked_posts_file = os.path.join(likes_dir, 'liked_posts.json')
                if os.path.exists(liked_posts_file):
                    with open(liked_posts_file, 'r') as file:
                        liked_posts_data = json.load(file)
                        for post in liked_posts_data['likes_media_likes']:
                            for data in post['string_list_data']:
                                liked_accounts.add(data['href'])

            # Check if 'saved' directory exists
            saved_dir = os.path.join(activity_dir, 'saved')
            if os.path.exists(saved_dir):
                # Check if 'saved_posts.json' file exists
                saved_posts_file = os.path.join(saved_dir, 'saved_posts.json')
                if os.path.exists(saved_posts_file):
                    with open(saved_posts_file, 'r') as file:
                        saved_posts_data = json.load(file)
                        for post in saved_posts_data['saved_saved_media']:
                            viewed_accounts.add(post['string_map_data']['Saved on']['href'])

        # Calculate viewed but not liked accounts
        viewed_but_not_liked_accounts = viewed_accounts - liked_accounts

        return viewed_but_not_liked_accounts

    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_to_csv(accounts, output_file):
    try:
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Account'])
            for account in accounts:
                writer.writerow([account])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        output_file = 'query_responses/results.csv'
        accounts = get_viewed_but_not_liked_accounts(root_dir)
        if accounts:
            write_to_csv(accounts, output_file)
        else:
            with open(output_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Account'])
    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()
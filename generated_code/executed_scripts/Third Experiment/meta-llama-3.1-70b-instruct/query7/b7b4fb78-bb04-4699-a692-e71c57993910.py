import os
import json
import csv

root_dir = "root_dir"

def get_user_engagement(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a dictionary to store user engagement
        user_engagement = {}

        # Check if the 'your_instagram_activity' directory exists
        activity_dir = os.path.join(root_dir, 'your_instagram_activity')
        if os.path.exists(activity_dir):
            # Check if the 'likes' directory exists
            likes_dir = os.path.join(activity_dir, 'likes')
            if os.path.exists(likes_dir):
                # Check if the 'liked_posts.json' file exists
                liked_posts_file = os.path.join(likes_dir, 'liked_posts.json')
                if os.path.exists(liked_posts_file):
                    with open(liked_posts_file, 'r') as file:
                        liked_posts_data = json.load(file)
                        for post in liked_posts_data['likes_media_likes']:
                            for data in post['string_list_data']:
                                user = data['href'].split('/')[-1]
                                if user not in user_engagement:
                                    user_engagement[user] = 1
                                else:
                                    user_engagement[user] += 1

        # Check if the 'your_instagram_activity' directory exists
        activity_dir = os.path.join(root_dir, 'your_instagram_activity')
        if os.path.exists(activity_dir):
            # Check if the 'saved' directory exists
            saved_dir = os.path.join(activity_dir, 'saved')
            if os.path.exists(saved_dir):
                # Check if the 'saved_posts.json' file exists
                saved_posts_file = os.path.join(saved_dir, 'saved_posts.json')
                if os.path.exists(saved_posts_file):
                    with open(saved_posts_file, 'r') as file:
                        saved_posts_data = json.load(file)
                        for post in saved_posts_data['saved_saved_media']:
                            user = post['string_map_data']['Saved on']['href'].split('/')[-1]
                            if user not in user_engagement:
                                user_engagement[user] = 1
                            else:
                                user_engagement[user] += 1

        return user_engagement

    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_to_csv(user_engagement):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['User', 'Times Engaged'])
            for user, engagement in user_engagement.items():
                writer.writerow([user, engagement])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        user_engagement = get_user_engagement(root_dir)
        if user_engagement:
            write_to_csv(user_engagement)
        else:
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['User', 'Times Engaged'])
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()
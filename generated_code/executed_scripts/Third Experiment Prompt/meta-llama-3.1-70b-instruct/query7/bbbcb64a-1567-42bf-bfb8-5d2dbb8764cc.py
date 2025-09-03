import os
import json
import csv

root_dir = "root_dir"

def get_engagement_data(root_dir):
    engagement_data = {}
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Navigate to the 'your_instagram_activity' directory
        activity_dir = os.path.join(root_dir, "your_instagram_activity")
        if not os.path.exists(activity_dir):
            raise FileNotFoundError("FileNotFoundError: The 'your_instagram_activity' directory does not exist.")

        # Navigate to the 'likes' directory
        likes_dir = os.path.join(activity_dir, "likes")
        if not os.path.exists(likes_dir):
            raise FileNotFoundError("FileNotFoundError: The 'likes' directory does not exist.")

        # Open the 'liked_posts.json' file
        liked_posts_file = os.path.join(likes_dir, "liked_posts.json")
        if not os.path.exists(liked_posts_file):
            raise FileNotFoundError("FileNotFoundError: The 'liked_posts.json' file does not exist.")

        with open(liked_posts_file, "r", encoding="utf-8") as file:
            liked_posts_data = json.load(file)

        # Extract engagement data
        for post in liked_posts_data["likes_media_likes"]:
            for like in post["string_list_data"]:
                user = like["value"]
                if user not in engagement_data:
                    engagement_data[user] = 0
                engagement_data[user] += 1

    except FileNotFoundError as e:
        raise e

    return engagement_data

def write_csv(engagement_data):
    with open("query_responses/results.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["User", "Times Engaged"])
        for user, times_engaged in engagement_data.items():
            writer.writerow([user, times_engaged])

def main():
    engagement_data = get_engagement_data(root_dir)
    if engagement_data:
        write_csv(engagement_data)
    else:
        # Write column headers only if no engagement data is found
        with open("query_responses/results.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Times Engaged"])

if __name__ == "__main__":
    main()
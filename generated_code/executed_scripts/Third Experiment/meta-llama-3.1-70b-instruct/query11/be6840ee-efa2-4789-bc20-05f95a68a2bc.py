import os
import csv

root_dir = "root_dir"

def get_viewed_posts(root_dir):
    try:
        posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        if not os.path.exists(posts_viewed_path):
            raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")
        with open(posts_viewed_path, 'r') as file:
            posts_viewed_data = eval(file.read())
            viewed_posts = [post["string_map_data"]["Author"]["value"] for post in posts_viewed_data["impressions_history_posts_seen"]]
            return viewed_posts
    except Exception as e:
        raise ValueError("Error: " + str(e))

def get_liked_posts(root_dir):
    try:
        story_likes_path = os.path.join(root_dir, "story_activities", "story_likes.json")
        if not os.path.exists(story_likes_path):
            raise FileNotFoundError("FileNotFoundError: The story_likes.json file does not exist.")
        with open(story_likes_path, 'r') as file:
            story_likes_data = eval(file.read())
            liked_posts = [post["title"] for post in story_likes_data["story_activities_story_likes"]]
            return liked_posts
    except Exception as e:
        raise ValueError("Error: " + str(e))

def get_accounts(root_dir):
    try:
        viewed_posts = get_viewed_posts(root_dir)
        liked_posts = get_liked_posts(root_dir)
        accounts = [post for post in viewed_posts if post not in liked_posts]
        return accounts
    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_to_csv(accounts):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Account"])
            for account in accounts:
                writer.writerow([account])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        if not os.path.exists(os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")) and not os.path.exists(os.path.join(root_dir, "story_activities", "story_likes.json")):
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Account"])
            return
        accounts = get_accounts(root_dir)
        write_to_csv(accounts)
    except Exception as e:
        if "FileNotFoundError" in str(e):
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Account"])
        else:
            raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()
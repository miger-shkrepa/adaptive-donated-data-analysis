import os
import json
import csv
from collections import defaultdict

root_dir = "root_dir"

def get_interacted_accounts(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize dictionaries to store interaction counts
        post_likes = defaultdict(int)
        story_likes = defaultdict(int)
        comments = defaultdict(int)

        # Iterate over the directory structure
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename == "liked_posts.json":
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        for like in data["likes_media_likes"]:
                            post_likes[like["title"]] += 1
                elif filename == "liked_comments.json":
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        for like in data["likes_comment_likes"]:
                            comments[like["title"]] += 1

        # Combine interaction counts into a single dictionary
        interacted_accounts = defaultdict(lambda: [0, 0, 0])
        for account, count in post_likes.items():
            interacted_accounts[account][0] = count
        for account, count in story_likes.items():
            interacted_accounts[account][1] = count
        for account, count in comments.items():
            interacted_accounts[account][2] = count

        # Get the top 20 interacted accounts
        top_accounts = sorted(interacted_accounts.items(), key=lambda x: sum(x[1]), reverse=True)[:20]

        return top_accounts

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(accounts):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
            for account, counts in accounts:
                writer.writerow([account] + counts)

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        accounts = get_interacted_accounts(root_dir)
        save_to_csv(accounts)
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()
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

        # Initialize dictionaries to store the interaction counts
        post_likes = defaultdict(int)
        story_likes = defaultdict(int)
        comments = defaultdict(int)

        # Iterate over the files in the likes directory
        likes_dir = os.path.join(root_dir, "likes")
        if os.path.exists(likes_dir):
            for filename in os.listdir(likes_dir):
                if filename == "liked_posts.json":
                    with open(os.path.join(likes_dir, filename), "r") as file:
                        data = json.load(file)
                        for like in data["likes_media_likes"]:
                            for item in like["string_list_data"]:
                                post_likes[item["value"]] += 1
                elif filename == "liked_comments.json":
                    with open(os.path.join(likes_dir, filename), "r") as file:
                        data = json.load(file)
                        for like in data["likes_comment_likes"]:
                            for item in like["string_list_data"]:
                                comments[item["value"]] += 1

        # Iterate over the files in the messages directory
        messages_dir = os.path.join(root_dir, "messages", "inbox", "conversation")
        if os.path.exists(messages_dir):
            for filename in os.listdir(messages_dir):
                if filename.endswith(".json"):
                    with open(os.path.join(messages_dir, filename), "r") as file:
                        data = json.load(file)
                        for message in data["messages"]:
                            if "sender_name" in message:
                                comments[message["sender_name"]] += 1

        # Combine the interaction counts into a single dictionary
        interacted_accounts = {}
        for account in set(list(post_likes.keys()) + list(story_likes.keys()) + list(comments.keys())):
            interacted_accounts[account] = {
                "Post Likes": post_likes.get(account, 0),
                "Story Likes": story_likes.get(account, 0),
                "Comments": comments.get(account, 0)
            }

        # Sort the interacted accounts by total interactions and get the top 20
        top_accounts = sorted(interacted_accounts.items(), key=lambda x: sum(x[1].values()), reverse=True)[:20]

        return top_accounts

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(accounts, filename):
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
            for account, interactions in accounts:
                writer.writerow([account, interactions["Post Likes"], interactions["Story Likes"], interactions["Comments"]])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        accounts = get_interacted_accounts(root_dir)
        save_to_csv(accounts, "query_responses/results.csv")
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()
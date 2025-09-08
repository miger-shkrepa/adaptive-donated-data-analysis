import os
import json
import csv

root_dir = "root_dir"

def get_interacted_accounts(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize dictionaries to store interaction counts
        post_likes = {}
        story_likes = {}
        comments = {}

        # Iterate over messages directory
        messages_dir = os.path.join(root_dir, "messages")
        if os.path.exists(messages_dir):
            for username in os.listdir(os.path.join(messages_dir, "inbox")):
                inbox_dir = os.path.join(messages_dir, "inbox", username)
                for filename in os.listdir(inbox_dir):
                    if filename.endswith(".json"):
                        with open(os.path.join(inbox_dir, filename), "r") as file:
                            data = json.load(file)
                            for message in data["messages"]:
                                if message["sender_name"] != "str":
                                    comments[message["sender_name"]] = comments.get(message["sender_name"], 0) + 1

        # Iterate over likes directory
        likes_dir = os.path.join(root_dir, "personal_information", "likes")
        if os.path.exists(likes_dir):
            for filename in os.listdir(likes_dir):
                if filename.endswith(".json"):
                    with open(os.path.join(likes_dir, filename), "r") as file:
                        data = json.load(file)
                        for like in data["likes_media_likes"] if filename == "liked_posts.json" else data["likes_comment_likes"]:
                            for item in like["string_list_data"]:
                                if item["value"] != "str":
                                    if filename == "liked_posts.json":
                                        post_likes[item["value"]] = post_likes.get(item["value"], 0) + 1
                                    else:
                                        story_likes[item["value"]] = story_likes.get(item["value"], 0) + 1

        # Combine interaction counts
        interacted_accounts = {}
        for account, count in post_likes.items():
            interacted_accounts[account] = interacted_accounts.get(account, 0) + count
        for account, count in story_likes.items():
            interacted_accounts[account] = interacted_accounts.get(account, 0) + count
        for account, count in comments.items():
            interacted_accounts[account] = interacted_accounts.get(account, 0) + count

        # Get top 20 interacted accounts
        top_accounts = sorted(interacted_accounts.items(), key=lambda x: x[1], reverse=True)[:20]

        return top_accounts

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(accounts):
    with open("query_responses/results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
        for account, _ in accounts:
            writer.writerow([account, 0, 0, 0])

def main():
    try:
        accounts = get_interacted_accounts(root_dir)
        save_to_csv(accounts)
    except Exception as e:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()
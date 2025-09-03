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

        # Process post likes
        post_likes_path = os.path.join(root_dir, "likes", "liked_posts.json")
        if os.path.exists(post_likes_path):
            with open(post_likes_path, "r") as file:
                data = json.load(file)
                for item in data["likes_media_likes"]:
                    for value in item["string_list_data"]:
                        username = value["value"]
                        post_likes[username] = post_likes.get(username, 0) + 1

        # Process story likes
        story_likes_path = os.path.join(root_dir, "story_interactions", "story_likes.json")
        if os.path.exists(story_likes_path):
            with open(story_likes_path, "r") as file:
                data = json.load(file)
                for item in data["story_activities_story_likes"]:
                    for value in item["string_list_data"]:
                        username = value["value"]
                        story_likes[username] = story_likes.get(username, 0) + 1

        # Process comments
        messages_path = os.path.join(root_dir, "messages", "inbox")
        if os.path.exists(messages_path):
            for username in os.listdir(messages_path):
                user_path = os.path.join(messages_path, username)
                for file in os.listdir(user_path):
                    file_path = os.path.join(user_path, file)
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        for message in data["messages"]:
                            if "sender_name" in message:
                                sender = message["sender_name"]
                                comments[sender] = comments.get(sender, 0) + 1

        # Combine interaction counts
        interacted_accounts = {}
        for username in set(list(post_likes.keys()) + list(story_likes.keys()) + list(comments.keys())):
            interacted_accounts[username] = post_likes.get(username, 0) + story_likes.get(username, 0) + comments.get(username, 0)

        # Get top 20 interacted accounts
        top_accounts = sorted(interacted_accounts.items(), key=lambda x: x[1], reverse=True)[:20]

        return top_accounts

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(accounts):
    with open("query_responses/results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
        for account in accounts:
            writer.writerow([account[0], 0, 0, account[1]])

def main():
    try:
        accounts = get_interacted_accounts(root_dir)
        save_to_csv(accounts)
    except Exception as e:
        print("Error: " + str(e))
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])

if __name__ == "__main__":
    main()
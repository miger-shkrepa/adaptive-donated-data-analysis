import os
import json
import csv

root_dir = "root_dir"

def get_interacted_accounts(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        interacted_accounts = {}

        # Process post likes
        post_likes_path = os.path.join(root_dir, "likes", "liked_posts.json")
        if os.path.exists(post_likes_path):
            with open(post_likes_path, "r") as file:
                post_likes_data = json.load(file)
                for post_like in post_likes_data["likes_media_likes"]:
                    for string_list_data in post_like.get("string_list_data", []):
                        account = string_list_data.get("value")
                        if account:
                            interacted_accounts[account] = interacted_accounts.get(account, 0) + 1

        # Process story likes
        story_likes_path = os.path.join(root_dir, "story_activities_story_likes")
        if os.path.exists(story_likes_path):
            for filename in os.listdir(story_likes_path):
                file_path = os.path.join(story_likes_path, filename)
                if os.path.isfile(file_path):
                    with open(file_path, "r") as file:
                        story_likes_data = json.load(file)
                        for story_like in story_likes_data["story_activities_story_likes"]:
                            account = story_like.get("title")
                            if account:
                                interacted_accounts[account] = interacted_accounts.get(account, 0) + 1

        # Process comments
        messages_path = os.path.join(root_dir, "messages")
        if os.path.exists(messages_path):
            for username in os.listdir(messages_path):
                username_path = os.path.join(messages_path, username)
                if os.path.isdir(username_path):
                    for filename in os.listdir(username_path):
                        file_path = os.path.join(username_path, filename)
                        if os.path.isfile(file_path):
                            with open(file_path, "r") as file:
                                messages_data = json.load(file)
                                for message in messages_data.get("messages", []):
                                    account = message.get("sender_name")
                                    if account:
                                        interacted_accounts[account] = interacted_accounts.get(account, 0) + 1

        # Get top 20 interacted accounts
        top_interacted_accounts = sorted(interacted_accounts.items(), key=lambda x: x[1], reverse=True)[:20]

        return top_interacted_accounts

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(interacted_accounts):
    try:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
            for account, count in interacted_accounts:
                writer.writerow([account, 0, 0, count])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        interacted_accounts = get_interacted_accounts(root_dir)
        save_to_csv(interacted_accounts)

    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: " + str(e))
    except ValueError as e:
        raise ValueError("Error: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()
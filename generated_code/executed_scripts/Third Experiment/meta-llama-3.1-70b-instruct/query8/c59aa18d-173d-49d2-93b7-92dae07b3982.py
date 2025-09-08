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

        # Process liked posts
        liked_posts_path = os.path.join(root_dir, "likes", "liked_posts.json")
        if os.path.exists(liked_posts_path):
            with open(liked_posts_path, "r") as file:
                liked_posts_data = json.load(file)
                for post in liked_posts_data["likes_media_likes"]:
                    for string_data in post["string_list_data"]:
                        account = string_data["value"]
                        if account not in post_likes:
                            post_likes[account] = 0
                        post_likes[account] += 1
        else:
            print("Warning: liked_posts.json not found. Assuming no post likes.")

        # Process story likes (not available in the provided structure)
        # Assuming story likes are not available
        print("Warning: story likes data not available. Assuming no story likes.")

        # Process comments (not available in the provided structure)
        # Assuming comments are not available
        print("Warning: comments data not available. Assuming no comments.")

        # Process messages (for comments)
        messages_path = os.path.join(root_dir, "messages")
        if os.path.exists(messages_path):
            for username in os.listdir(messages_path):
                message_path = os.path.join(messages_path, username, "message_1.json")
                if os.path.exists(message_path):
                    with open(message_path, "r") as file:
                        message_data = json.load(file)
                        for message in message_data["messages"]:
                            if "sender_name" in message:
                                account = message["sender_name"]
                                if account not in comments:
                                    comments[account] = 0
                                comments[account] += 1

        # Combine interaction counts
        interaction_counts = {}
        for account in set(list(post_likes.keys()) + list(story_likes.keys()) + list(comments.keys())):
            interaction_counts[account] = post_likes.get(account, 0) + story_likes.get(account, 0) + comments.get(account, 0)

        # Get top 20 interacted accounts
        top_accounts = sorted(interaction_counts.items(), key=lambda x: x[1], reverse=True)[:20]

        return top_accounts

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(accounts):
    with open("query_responses/results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
        for account, count in accounts:
            writer.writerow([account, 0, 0, 0])  # Assuming no story likes and comments

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
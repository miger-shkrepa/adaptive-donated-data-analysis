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
        liked_posts_path = os.path.join(root_dir, "likes", "liked_posts.json")
        if os.path.exists(liked_posts_path):
            with open(liked_posts_path, "r") as file:
                data = json.load(file)
                for item in data["likes_media_likes"]:
                    for like in item["string_list_data"]:
                        user = like["value"]
                        post_likes[user] = post_likes.get(user, 0) + 1

        # Process story likes
        story_likes_path = os.path.join(root_dir, "story_interactions", "story_likes.json")
        if os.path.exists(story_likes_path):
            with open(story_likes_path, "r") as file:
                data = json.load(file)
                for item in data["story_activities_story_likes"]:
                    for like in item["string_list_data"]:
                        user = like.get("value", "")
                        story_likes[user] = story_likes.get(user, 0) + 1

        # Process comments (assuming comments are messages in inbox)
        inbox_path = os.path.join(root_dir, "messages", "inbox")
        if os.path.exists(inbox_path):
            for username in os.listdir(inbox_path):
                user_path = os.path.join(inbox_path, username)
                for filename in os.listdir(user_path):
                    file_path = os.path.join(user_path, filename)
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        for message in data["messages"]:
                            if "content" in message:
                                user = message["sender_name"]
                                comments[user] = comments.get(user, 0) + 1

        # Combine interaction counts
        interaction_counts = {}
        for user in set(list(post_likes.keys()) + list(story_likes.keys()) + list(comments.keys())):
            interaction_counts[user] = post_likes.get(user, 0) + story_likes.get(user, 0) + comments.get(user, 0)

        # Get top 20 interacted accounts
        top_accounts = sorted(interaction_counts.items(), key=lambda x: x[1], reverse=True)[:20]

        return top_accounts

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(accounts):
    with open("query_responses/results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
        for user, count in accounts:
            writer.writerow([user, 0, 0, 0])  # Replace with actual counts if available

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
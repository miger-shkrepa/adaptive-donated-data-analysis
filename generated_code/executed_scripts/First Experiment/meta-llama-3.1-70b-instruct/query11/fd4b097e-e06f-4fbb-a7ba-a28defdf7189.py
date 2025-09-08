import os
import json
import csv

root_dir = "root_dir"

def get_viewed_posts_but_not_liked(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        viewed_posts = set()
        liked_posts = set()

        # Iterate over the messages folder
        messages_dir = os.path.join(root_dir, "messages", "inbox")
        if os.path.exists(messages_dir):
            for filename in os.listdir(messages_dir):
                if filename.endswith(".json"):
                    file_path = os.path.join(messages_dir, filename)
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        for message in data.get("messages", []):
                            if message.get("content", ""):
                                viewed_posts.add(message.get("sender_name", ""))

        # Iterate over the likes folder
        likes_dir = os.path.join(root_dir, "likes")
        if os.path.exists(likes_dir):
            for filename in os.listdir(likes_dir):
                if filename.endswith(".json"):
                    file_path = os.path.join(likes_dir, filename)
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        for like in data.get("likes_media_likes", []):
                            liked_posts.add(like.get("title", ""))

        # Find the accounts that have been viewed but not liked
        viewed_but_not_liked = viewed_posts - liked_posts

        # Save the results to a CSV file
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account"])
            for account in viewed_but_not_liked:
                writer.writerow([account])

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: Error parsing JSON - {e}")
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred - {e}")

get_viewed_posts_but_not_liked(root_dir)
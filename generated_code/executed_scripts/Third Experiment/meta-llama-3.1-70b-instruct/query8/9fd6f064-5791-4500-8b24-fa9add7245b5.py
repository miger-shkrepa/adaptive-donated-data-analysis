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
        liked_posts_path = os.path.join(root_dir, "connections", "likes", "liked_posts.json")
        if os.path.exists(liked_posts_path):
            with open(liked_posts_path, "r") as file:
                liked_posts_data = json.load(file)
                for post in liked_posts_data["likes_media_likes"]:
                    for string_data in post["string_list_data"]:
                        username = string_data["value"]
                        if username not in post_likes:
                            post_likes[username] = 1
                        else:
                            post_likes[username] += 1

        # Process liked comments
        liked_comments_path = os.path.join(root_dir, "connections", "likes", "liked_comments.json")
        if os.path.exists(liked_comments_path):
            with open(liked_comments_path, "r") as file:
                liked_comments_data = json.load(file)
                for comment in liked_comments_data["likes_comment_likes"]:
                    for string_data in comment["string_list_data"]:
                        username = string_data["value"]
                        if username not in comments:
                            comments[username] = 1
                        else:
                            comments[username] += 1

        # Process stories
        stories_path = os.path.join(root_dir, "connections", "followers_and_following", "stories.json")
        if os.path.exists(stories_path):
            with open(stories_path, "r") as file:
                stories_data = json.load(file)
                for story in stories_data["ig_stories"]:
                    username = story["title"]
                    if username not in story_likes:
                        story_likes[username] = 1
                    else:
                        story_likes[username] += 1

        # Combine interaction counts
        interaction_counts = {}
        for username in set(list(post_likes.keys()) + list(story_likes.keys()) + list(comments.keys())):
            interaction_counts[username] = post_likes.get(username, 0) + story_likes.get(username, 0) + comments.get(username, 0)

        # Get top 20 interacted accounts
        top_interacted_accounts = sorted(interaction_counts.items(), key=lambda x: x[1], reverse=True)[:20]

        return top_interacted_accounts

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(interacted_accounts):
    try:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
            for account in interacted_accounts:
                writer.writerow([account[0], 0, 0, account[1]])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        interacted_accounts = get_interacted_accounts(root_dir)
        save_to_csv(interacted_accounts)

    except FileNotFoundError as e:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
        raise FileNotFoundError("FileNotFoundError: " + str(e))

    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()
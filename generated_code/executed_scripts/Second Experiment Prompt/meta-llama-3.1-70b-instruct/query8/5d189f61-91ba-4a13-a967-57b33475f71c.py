import os
import json
import csv

root_dir = "root_dir"

def get_interacted_accounts(root_dir):
    interacted_accounts = {}
    try:
        # Get post likes
        post_likes_file = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        if os.path.exists(post_likes_file):
            with open(post_likes_file, 'r') as f:
                post_likes_data = json.load(f)
                for post_like in post_likes_data.get("likes_media_likes", []):
                    user = post_like.get("title")
                    if user:
                        if user in interacted_accounts:
                            interacted_accounts[user]["Post Likes"] += 1
                        else:
                            interacted_accounts[user] = {"Post Likes": 1, "Story Likes": 0, "Comments": 0}
        else:
            print("Warning: liked_posts.json file not found.")

        # Get story likes
        story_likes_file = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
        if os.path.exists(story_likes_file):
            with open(story_likes_file, 'r') as f:
                story_likes_data = json.load(f)
                for story_like in story_likes_data.get("story_activities_story_likes", []):
                    user = story_like.get("title")
                    if user:
                        if user in interacted_accounts:
                            interacted_accounts[user]["Story Likes"] += 1
                        else:
                            interacted_accounts[user] = {"Post Likes": 0, "Story Likes": 1, "Comments": 0}
        else:
            print("Warning: story_likes.json file not found.")

        # Get comments
        comments_file = os.path.join(root_dir, "your_instagram_activity", "comments", "reels_comments.json")
        if os.path.exists(comments_file):
            with open(comments_file, 'r') as f:
                comments_data = json.load(f)
                for comment in comments_data.get("comments_reels_comments", []):
                    user = comment.get("string_map_data", {}).get("Media Owner", {}).get("value")
                    if user:
                        if user in interacted_accounts:
                            interacted_accounts[user]["Comments"] += 1
                        else:
                            interacted_accounts[user] = {"Post Likes": 0, "Story Likes": 0, "Comments": 1}
        else:
            print("Warning: reels_comments.json file not found.")

        # Sort interacted accounts by total interactions
        sorted_interacted_accounts = sorted(interacted_accounts.items(), key=lambda x: sum(x[1].values()), reverse=True)

        # Get top 20 interacted accounts
        top_interacted_accounts = sorted_interacted_accounts[:20]

        return top_interacted_accounts

    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory does not exist.")
    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(interacted_accounts):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ["User", "Post Likes", "Story Likes", "Comments"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account in interacted_accounts:
            writer.writerow({"User": account[0], "Post Likes": account[1]["Post Likes"], "Story Likes": account[1]["Story Likes"], "Comments": account[1]["Comments"]})

def main():
    interacted_accounts = get_interacted_accounts(root_dir)
    if interacted_accounts:
        save_to_csv(interacted_accounts)
    else:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ["User", "Post Likes", "Story Likes", "Comments"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

if __name__ == "__main__":
    main()
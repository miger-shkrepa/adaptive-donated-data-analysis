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
            with open(post_likes_file, "r") as f:
                post_likes_data = json.load(f)
                for post_like in post_likes_data["likes_media_likes"]:
                    user = post_like["title"]
                    if user not in interacted_accounts:
                        interacted_accounts[user] = {"post_likes": 0, "story_likes": 0, "comments": 0}
                    interacted_accounts[user]["post_likes"] += 1
        else:
            print(f"Warning: {post_likes_file} not found. Assuming 0 post likes.")

        # Get story likes
        story_likes_file = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
        if os.path.exists(story_likes_file):
            with open(story_likes_file, "r") as f:
                story_likes_data = json.load(f)
                for story_like in story_likes_data["story_activities_story_likes"]:
                    user = story_like["title"]
                    if user not in interacted_accounts:
                        interacted_accounts[user] = {"post_likes": 0, "story_likes": 0, "comments": 0}
                    interacted_accounts[user]["story_likes"] += 1
        else:
            print(f"Warning: {story_likes_file} not found. Assuming 0 story likes.")

        # Get comments
        comments_file = os.path.join(root_dir, "your_instagram_activity", "comments", "reels_comments.json")
        if os.path.exists(comments_file):
            with open(comments_file, "r") as f:
                comments_data = json.load(f)
                for comment in comments_data["comments_reels_comments"]:
                    user = comment["string_map_data"]["Media Owner"]["value"]
                    if user not in interacted_accounts:
                        interacted_accounts[user] = {"post_likes": 0, "story_likes": 0, "comments": 0}
                    interacted_accounts[user]["comments"] += 1
        else:
            print(f"Warning: {comments_file} not found. Assuming 0 comments.")

        # Sort interacted accounts by total interactions
        sorted_accounts = sorted(interacted_accounts.items(), key=lambda x: sum(x[1].values()), reverse=True)

        # Get top 20 accounts
        top_accounts = sorted_accounts[:20]

        return top_accounts

    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory does not exist.")
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

def save_to_csv(accounts):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
        for account in accounts:
            writer.writerow([account[0], account[1]["post_likes"], account[1]["story_likes"], account[1]["comments"]])

def main():
    try:
        accounts = get_interacted_accounts(root_dir)
        save_to_csv(accounts)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
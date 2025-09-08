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
                    account = post_like["title"]
                    if account in interacted_accounts:
                        interacted_accounts[account]["post_likes"] += 1
                    else:
                        interacted_accounts[account] = {"post_likes": 1, "story_likes": 0, "comments": 0}
        else:
            print("Warning: liked_posts.json file not found.")

        # Get story likes
        story_likes_file = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
        if os.path.exists(story_likes_file):
            with open(story_likes_file, "r") as f:
                story_likes_data = json.load(f)
                for story_like in story_likes_data["story_activities_story_likes"]:
                    account = story_like["title"]
                    if account in interacted_accounts:
                        interacted_accounts[account]["story_likes"] += 1
                    else:
                        interacted_accounts[account] = {"post_likes": 0, "story_likes": 1, "comments": 0}
        else:
            print("Warning: story_likes.json file not found.")

        # Get comments
        comments_file = os.path.join(root_dir, "your_instagram_activity", "comments", "reels_comments.json")
        if os.path.exists(comments_file):
            with open(comments_file, "r") as f:
                comments_data = json.load(f)
                for comment in comments_data["comments_reels_comments"]:
                    account = comment["string_map_data"]["Media Owner"]["value"]
                    if account in interacted_accounts:
                        interacted_accounts[account]["comments"] += 1
                    else:
                        interacted_accounts[account] = {"post_likes": 0, "story_likes": 0, "comments": 1}
        else:
            print("Warning: reels_comments.json file not found.")

        # Sort interacted accounts by total interactions
        sorted_accounts = sorted(interacted_accounts.items(), key=lambda x: x[1]["post_likes"] + x[1]["story_likes"] + x[1]["comments"], reverse=True)

        return sorted_accounts[:20]

    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory does not exist.")
    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(interacted_accounts):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        fieldnames = ["User", "Post Likes", "Story Likes", "Comments"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, interactions in interacted_accounts:
            writer.writerow({"User": account, "Post Likes": interactions["post_likes"], "Story Likes": interactions["story_likes"], "Comments": interactions["comments"]})

if __name__ == "__main__":
    interacted_accounts = get_interacted_accounts(root_dir)
    if interacted_accounts:
        save_to_csv(interacted_accounts)
    else:
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            fieldnames = ["User", "Post Likes", "Story Likes", "Comments"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
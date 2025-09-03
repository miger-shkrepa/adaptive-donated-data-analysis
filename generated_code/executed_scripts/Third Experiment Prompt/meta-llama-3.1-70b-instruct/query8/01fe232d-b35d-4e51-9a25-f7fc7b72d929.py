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
                        interacted_accounts[user] = {"Post Likes": 0, "Story Likes": 0, "Comments": 0}
                    interacted_accounts[user]["Post Likes"] += 1
        else:
            print("Warning: liked_posts.json not found. Assuming no post likes.")

        # Get story likes
        story_likes_file = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
        if os.path.exists(story_likes_file):
            with open(story_likes_file, "r") as f:
                story_likes_data = json.load(f)
                for story_like in story_likes_data["story_activities_story_likes"]:
                    user = story_like["title"]
                    if user not in interacted_accounts:
                        interacted_accounts[user] = {"Post Likes": 0, "Story Likes": 0, "Comments": 0}
                    interacted_accounts[user]["Story Likes"] += 1
        else:
            print("Warning: story_likes.json not found. Assuming no story likes.")

        # Get comments
        comments_file = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_comments.json")
        if os.path.exists(comments_file):
            with open(comments_file, "r") as f:
                comments_data = json.load(f)
                for comment in comments_data["likes_comment_likes"]:
                    user = comment["title"]
                    if user not in interacted_accounts:
                        interacted_accounts[user] = {"Post Likes": 0, "Story Likes": 0, "Comments": 0}
                    interacted_accounts[user]["Comments"] += 1
        else:
            print("Warning: liked_comments.json not found. Assuming no comments.")

        # Sort interacted accounts by total interactions
        sorted_accounts = sorted(interacted_accounts.items(), key=lambda x: sum(x[1].values()), reverse=True)

        # Write to CSV file
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
            for account in sorted_accounts[:20]:
                writer.writerow([account[0], account[1]["Post Likes"], account[1]["Story Likes"], account[1]["Comments"]])

    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory does not exist.")
    except Exception as e:
        raise ValueError("Error: " + str(e))

get_interacted_accounts(root_dir)
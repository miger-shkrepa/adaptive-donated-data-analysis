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
            with open(post_likes_file, "r", encoding="utf-8") as f:
                post_likes_data = json.load(f)
                for post_like in post_likes_data["likes_media_likes"]:
                    if "string_list_data" in post_like:
                        for data in post_like["string_list_data"]:
                            if "value" in data:
                                account = data["value"]
                                if account in interacted_accounts:
                                    interacted_accounts[account]["post_likes"] += 1
                                else:
                                    interacted_accounts[account] = {"post_likes": 1, "story_likes": 0, "comments": 0}
        else:
            print("Warning: liked_posts.json file not found.")

        # Get story likes
        story_likes_file = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
        if os.path.exists(story_likes_file):
            with open(story_likes_file, "r", encoding="utf-8") as f:
                story_likes_data = json.load(f)
                for story_like in story_likes_data["story_activities_story_likes"]:
                    if "string_list_data" in story_like:
                        for data in story_like["string_list_data"]:
                            if "timestamp" in data:
                                account = story_like["title"]
                                if account in interacted_accounts:
                                    interacted_accounts[account]["story_likes"] += 1
                                else:
                                    interacted_accounts[account] = {"post_likes": 0, "story_likes": 1, "comments": 0}
        else:
            print("Warning: story_likes.json file not found.")

        # Get comments
        comments_file = os.path.join(root_dir, "your_instagram_activity", "comments", "post_comments_1.json")
        if os.path.exists(comments_file):
            with open(comments_file, "r", encoding="utf-8") as f:
                comments_data = json.load(f)
                for comment in comments_data:
                    if "string_map_data" in comment:
                        for data in comment["string_map_data"]:
                            if "value" in data:
                                account = comment["title"]
                                if account in interacted_accounts:
                                    interacted_accounts[account]["comments"] += 1
                                else:
                                    interacted_accounts[account] = {"post_likes": 0, "story_likes": 0, "comments": 1}
        else:
            print("Warning: post_comments_1.json file not found.")

        # Sort interacted accounts by total interactions
        sorted_accounts = sorted(interacted_accounts.items(), key=lambda x: sum(x[1].values()), reverse=True)

        # Write to CSV file
        with open("query_responses/results.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
            for account, interactions in sorted_accounts[:20]:
                writer.writerow([account, interactions["post_likes"], interactions["story_likes"], interactions["comments"]])

    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory does not exist.")
    except Exception as e:
        raise ValueError("Error: " + str(e))

get_interacted_accounts(root_dir)
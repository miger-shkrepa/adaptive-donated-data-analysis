import os
import json
import csv

root_dir = "root_dir"

def get_interacted_accounts(root_dir):
    interacted_accounts = {}
    try:
        # Get post likes
        post_likes_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        if os.path.exists(post_likes_path):
            with open(post_likes_path, 'r', encoding='utf-8') as f:
                post_likes_data = json.load(f)
                for post_like in post_likes_data["likes_media_likes"]:
                    media_owner = post_like["string_list_data"][0]["value"]
                    if media_owner in interacted_accounts:
                        interacted_accounts[media_owner]["post_likes"] += 1
                    else:
                        interacted_accounts[media_owner] = {"post_likes": 1, "story_likes": 0, "comments": 0}
        else:
            print("Warning: liked_posts.json not found. Assuming no post likes.")

        # Get story likes
        story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
        if os.path.exists(story_likes_path):
            with open(story_likes_path, 'r', encoding='utf-8') as f:
                story_likes_data = json.load(f)
                for story_like in story_likes_data["story_activities_story_likes"]:
                    media_owner = story_like["string_list_data"][0]["value"]
                    if media_owner in interacted_accounts:
                        interacted_accounts[media_owner]["story_likes"] += 1
                    else:
                        interacted_accounts[media_owner] = {"post_likes": 0, "story_likes": 1, "comments": 0}
        else:
            print("Warning: story_likes.json not found. Assuming no story likes.")

        # Get comments
        comments_path = os.path.join(root_dir, "your_instagram_activity", "comments", "reels_comments.json")
        if os.path.exists(comments_path):
            with open(comments_path, 'r', encoding='utf-8') as f:
                comments_data = json.load(f)
                for comment in comments_data["comments_reels_comments"]:
                    media_owner = comment["string_map_data"]["Media Owner"]["value"]
                    if media_owner in interacted_accounts:
                        interacted_accounts[media_owner]["comments"] += 1
                    else:
                        interacted_accounts[media_owner] = {"post_likes": 0, "story_likes": 0, "comments": 1}
        else:
            print("Warning: reels_comments.json not found. Assuming no comments.")

        # Sort interacted accounts by total interactions
        sorted_accounts = sorted(interacted_accounts.items(), key=lambda x: x[1]["post_likes"] + x[1]["story_likes"] + x[1]["comments"], reverse=True)

        return sorted_accounts[:20]

    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory does not exist.")
    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_csv(sorted_accounts):
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["User", "Post Likes", "Story Likes", "Comments"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account in sorted_accounts:
            writer.writerow({"User": account[0], "Post Likes": account[1]["post_likes"], "Story Likes": account[1]["story_likes"], "Comments": account[1]["comments"]})

sorted_accounts = get_interacted_accounts(root_dir)
write_csv(sorted_accounts)
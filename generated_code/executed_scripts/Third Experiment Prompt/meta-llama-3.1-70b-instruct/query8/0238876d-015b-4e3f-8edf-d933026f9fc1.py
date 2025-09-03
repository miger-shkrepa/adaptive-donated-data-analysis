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
                    for string_list_data in post_like["string_list_data"]:
                        account = string_list_data["value"]
                        if account in interacted_accounts:
                            interacted_accounts[account]["Post Likes"] += 1
                        else:
                            interacted_accounts[account] = {"Post Likes": 1, "Story Likes": 0, "Comments": 0}
        else:
            print("Warning: liked_posts.json not found. Treating post likes as 0.")

        # Get story likes
        story_likes_file = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_comments.json")
        if os.path.exists(story_likes_file):
            with open(story_likes_file, "r", encoding="utf-8") as f:
                story_likes_data = json.load(f)
                for story_like in story_likes_data["likes_comment_likes"]:
                    for string_list_data in story_like["string_list_data"]:
                        account = string_list_data["value"]
                        if account in interacted_accounts:
                            interacted_accounts[account]["Story Likes"] += 1
                        else:
                            interacted_accounts[account] = {"Post Likes": 0, "Story Likes": 1, "Comments": 0}
        else:
            print("Warning: liked_comments.json not found. Treating story likes as 0.")

        # Get comments
        comments_file = os.path.join(root_dir, "your_instagram_activity", "comments", "post_comments_1.json")
        if os.path.exists(comments_file):
            with open(comments_file, "r", encoding="utf-8") as f:
                comments_data = json.load(f)
                for comment in comments_data:
                    for string_map_data in comment["string_map_data"]:
                        if string_map_data == "Comment":
                            account = comment["string_map_data"][string_map_data]["value"]
                            if account in interacted_accounts:
                                interacted_accounts[account]["Comments"] += 1
                            else:
                                interacted_accounts[account] = {"Post Likes": 0, "Story Likes": 0, "Comments": 1}
        else:
            print("Warning: post_comments_1.json not found. Treating comments as 0.")

        # Get reels comments
        reels_comments_file = os.path.join(root_dir, "your_instagram_activity", "comments", "reels_comments.json")
        if os.path.exists(reels_comments_file):
            with open(reels_comments_file, "r", encoding="utf-8") as f:
                reels_comments_data = json.load(f)
                for reels_comment in reels_comments_data["comments_reels_comments"]:
                    for string_map_data in reels_comment["string_map_data"]:
                        if string_map_data == "Comment":
                            account = reels_comment["string_map_data"][string_map_data]["value"]
                            if account in interacted_accounts:
                                interacted_accounts[account]["Comments"] += 1
                            else:
                                interacted_accounts[account] = {"Post Likes": 0, "Story Likes": 0, "Comments": 1}
        else:
            print("Warning: reels_comments.json not found. Treating reels comments as 0.")

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
    with open("query_responses/results.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["User", "Post Likes", "Story Likes", "Comments"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, interactions in interacted_accounts:
            writer.writerow({"User": account, "Post Likes": interactions["Post Likes"], "Story Likes": interactions["Story Likes"], "Comments": interactions["Comments"]})

def main():
    interacted_accounts = get_interacted_accounts(root_dir)
    if interacted_accounts:
        save_to_csv(interacted_accounts)
    else:
        with open("query_responses/results.csv", "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["User", "Post Likes", "Story Likes", "Comments"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

if __name__ == "__main__":
    main()
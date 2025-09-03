import os
import json
import csv

root_dir = "root_dir"

def get_interacted_accounts(root_dir):
    interacted_accounts = {}
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Get liked posts
        liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        if os.path.exists(liked_posts_path):
            with open(liked_posts_path, "r") as f:
                liked_posts_data = json.load(f)
                for post in liked_posts_data["likes_media_likes"]:
                    for interaction in post["string_list_data"]:
                        account = interaction["href"].split("/")[-2]
                        if account not in interacted_accounts:
                            interacted_accounts[account] = {"post_likes": 0, "story_likes": 0, "comments": 0}
                        interacted_accounts[account]["post_likes"] += 1

        # Get saved posts (story likes)
        saved_posts_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")
        if os.path.exists(saved_posts_path):
            with open(saved_posts_path, "r") as f:
                saved_posts_data = json.load(f)
                for post in saved_posts_data["saved_saved_media"]:
                    account = post["string_map_data"]["Saved on"]["href"].split("/")[-2]
                    if account not in interacted_accounts:
                        interacted_accounts[account] = {"post_likes": 0, "story_likes": 0, "comments": 0}
                    interacted_accounts[account]["story_likes"] += 1

        # Get comments (not available in the provided structure)
        # Assuming comments are not available, we'll set comments to 0 for all accounts
        for account in interacted_accounts:
            interacted_accounts[account]["comments"] = 0

        # Sort interacted accounts by total interactions
        sorted_accounts = sorted(interacted_accounts.items(), key=lambda x: sum(x[1].values()), reverse=True)[:20]

        return sorted_accounts

    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

def write_csv(sorted_accounts):
    csv_path = "query_responses/results.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
        for account, interactions in sorted_accounts:
            writer.writerow([account, interactions["post_likes"], interactions["story_likes"], interactions["comments"]])

sorted_accounts = get_interacted_accounts(root_dir)
if sorted_accounts:
    write_csv(sorted_accounts)
else:
    # Write only column headers if no data is available
    with open("query_responses/results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
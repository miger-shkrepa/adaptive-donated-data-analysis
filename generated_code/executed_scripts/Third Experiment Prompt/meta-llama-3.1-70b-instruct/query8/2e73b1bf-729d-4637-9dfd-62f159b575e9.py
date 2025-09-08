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
            with open(post_likes_file, 'r', encoding='utf-8') as f:
                post_likes_data = json.load(f)
                for post_like in post_likes_data["likes_media_likes"]:
                    account = post_like["string_list_data"][0]["value"]
                    if account in interacted_accounts:
                        interacted_accounts[account]["Post Likes"] += 1
                    else:
                        interacted_accounts[account] = {"Post Likes": 1, "Story Likes": 0, "Comments": 0}
        else:
            print("Warning: liked_posts.json file not found.")

        # Get story likes
        story_likes_file = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        if os.path.exists(story_likes_file):
            with open(story_likes_file, 'r', encoding='utf-8') as f:
                story_likes_data = json.load(f)
                for story_like in story_likes_data["likes_media_likes"]:
                    account = story_like["string_list_data"][0]["value"]
                    if account in interacted_accounts:
                        interacted_accounts[account]["Story Likes"] += 1
                    else:
                        interacted_accounts[account] = {"Post Likes": 0, "Story Likes": 1, "Comments": 0}
        else:
            print("Warning: liked_posts.json file not found.")

        # Get comments
        comments_file = os.path.join(root_dir, "your_instagram_activity", "comments", "post_comments_1.json")
        if os.path.exists(comments_file):
            with open(comments_file, 'r', encoding='utf-8') as f:
                comments_data = json.load(f)
                for comment in comments_data:
                    if "string_map_data" in comment and "Media Owner" in comment["string_map_data"]:
                        account = comment["string_map_data"]["Media Owner"]["value"]
                        if account in interacted_accounts:
                            interacted_accounts[account]["Comments"] += 1
                        else:
                            interacted_accounts[account] = {"Post Likes": 0, "Story Likes": 0, "Comments": 1}
        else:
            print("Warning: post_comments_1.json file not found.")

        # Get story comments
        story_comments_file = os.path.join(root_dir, "your_instagram_activity", "comments", "reels_comments.json")
        if os.path.exists(story_comments_file):
            with open(story_comments_file, 'r', encoding='utf-8') as f:
                story_comments_data = json.load(f)
                for story_comment in story_comments_data["comments_reels_comments"]:
                    if "string_map_data" in story_comment and "Media Owner" in story_comment["string_map_data"]:
                        account = story_comment["string_map_data"]["Media Owner"]["value"]
                        if account in interacted_accounts:
                            interacted_accounts[account]["Comments"] += 1
                        else:
                            interacted_accounts[account] = {"Post Likes": 0, "Story Likes": 0, "Comments": 1}
        else:
            print("Warning: reels_comments.json file not found.")

        # Sort interacted accounts by total interactions
        sorted_accounts = sorted(interacted_accounts.items(), key=lambda x: sum(x[1].values()), reverse=True)

        # Get top 20 interacted accounts
        top_20_accounts = sorted_accounts[:20]

        return top_20_accounts

    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory does not exist.")
    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(accounts):
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["User", "Post Likes", "Story Likes", "Comments"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, interactions in accounts:
            writer.writerow({"User": account, "Post Likes": interactions["Post Likes"], "Story Likes": interactions["Story Likes"], "Comments": interactions["Comments"]})

if __name__ == "__main__":
    accounts = get_interacted_accounts(root_dir)
    if accounts:
        save_to_csv(accounts)
    else:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["User", "Post Likes", "Story Likes", "Comments"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
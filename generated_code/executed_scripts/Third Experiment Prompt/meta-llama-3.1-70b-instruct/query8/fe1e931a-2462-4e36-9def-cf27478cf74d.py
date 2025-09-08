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
                    if "string_list_data" in post_like:
                        for data in post_like["string_list_data"]:
                            if "value" in data:
                                account = data["value"]
                                if account in interacted_accounts:
                                    interacted_accounts[account]["post_likes"] += 1
                                else:
                                    interacted_accounts[account] = {"post_likes": 1, "story_likes": 0, "comments": 0}
        else:
            raise FileNotFoundError("FileNotFoundError: liked_posts.json does not exist.")

        # Get story likes
        story_likes_file = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        if os.path.exists(story_likes_file):
            with open(story_likes_file, 'r', encoding='utf-8') as f:
                story_likes_data = json.load(f)
                for story_like in story_likes_data["likes_media_likes"]:
                    if "string_list_data" in story_like:
                        for data in story_like["string_list_data"]:
                            if "value" in data:
                                account = data["value"]
                                if account in interacted_accounts:
                                    interacted_accounts[account]["story_likes"] += 1
                                else:
                                    interacted_accounts[account] = {"post_likes": 0, "story_likes": 1, "comments": 0}
        else:
            raise FileNotFoundError("FileNotFoundError: liked_posts.json does not exist.")

        # Get comments
        comments_file = os.path.join(root_dir, "your_instagram_activity", "comments", "post_comments_1.json")
        if os.path.exists(comments_file):
            with open(comments_file, 'r', encoding='utf-8') as f:
                comments_data = json.load(f)
                for comment in comments_data:
                    if "string_map_data" in comment:
                        for data in comment["string_map_data"].values():
                            if "value" in data:
                                account = data["value"]
                                if account in interacted_accounts:
                                    interacted_accounts[account]["comments"] += 1
                                else:
                                    interacted_accounts[account] = {"post_likes": 0, "story_likes": 0, "comments": 1}
        else:
            raise FileNotFoundError("FileNotFoundError: post_comments_1.json does not exist.")

    except FileNotFoundError as e:
        raise e

    # Sort interacted accounts by total interactions
    sorted_accounts = sorted(interacted_accounts.items(), key=lambda x: sum(x[1].values()), reverse=True)

    return sorted_accounts[:20]

def save_to_csv(sorted_accounts):
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["User", "Post Likes", "Story Likes", "Comments"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, interactions in sorted_accounts:
            writer.writerow({"User": account, "Post Likes": interactions["post_likes"], "Story Likes": interactions["story_likes"], "Comments": interactions["comments"]})

def main():
    try:
        sorted_accounts = get_interacted_accounts(root_dir)
        save_to_csv(sorted_accounts)
    except FileNotFoundError as e:
        print(e)
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["User", "Post Likes", "Story Likes", "Comments"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

if __name__ == "__main__":
    main()
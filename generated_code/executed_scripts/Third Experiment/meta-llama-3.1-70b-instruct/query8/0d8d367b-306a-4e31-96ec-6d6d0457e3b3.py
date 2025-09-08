import os
import json
import csv

root_dir = "root_dir"

def get_interacted_accounts(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize dictionaries to store interaction counts
        post_likes = {}
        story_likes = {}
        comments = {}

        # Check if 'your_instagram_activity' directory exists
        activity_dir = os.path.join(root_dir, 'your_instagram_activity')
        if os.path.exists(activity_dir):
            # Check if 'likes' directory exists
            likes_dir = os.path.join(activity_dir, 'likes')
            if os.path.exists(likes_dir):
                # Check if 'liked_posts.json' file exists
                liked_posts_file = os.path.join(likes_dir, 'liked_posts.json')
                if os.path.exists(liked_posts_file):
                    with open(liked_posts_file, 'r') as file:
                        liked_posts_data = json.load(file)
                        for post in liked_posts_data['likes_media_likes']:
                            for interaction in post['string_list_data']:
                                account = interaction['href'].split('/')[-1]
                                if account not in post_likes:
                                    post_likes[account] = 0
                                post_likes[account] += 1

            # Check if 'story_likes' directory exists (not present in the given structure)
            # If it were present, we would process it similarly to 'likes'

            # Check if 'comments' directory exists (not present in the given structure)
            # If it were present, we would process it similarly to 'likes'

        # Since 'story_likes' and 'comments' directories are not present in the given structure,
        # we will treat their contributions as 0 and continue processing the rest using the available data.

        # Combine interaction counts
        interaction_counts = {}
        for account, count in post_likes.items():
            interaction_counts[account] = count
        for account, count in story_likes.items():
            interaction_counts[account] = interaction_counts.get(account, 0) + count
        for account, count in comments.items():
            interaction_counts[account] = interaction_counts.get(account, 0) + count

        # Get top 20 interacted accounts
        top_accounts = sorted(interaction_counts.items(), key=lambda x: x[1], reverse=True)[:20]

        return top_accounts

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(accounts, filename):
    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
            for account, count in accounts:
                writer.writerow([account, count, 0, 0])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        accounts = get_interacted_accounts(root_dir)
        save_to_csv(accounts, 'query_responses/results.csv')
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()
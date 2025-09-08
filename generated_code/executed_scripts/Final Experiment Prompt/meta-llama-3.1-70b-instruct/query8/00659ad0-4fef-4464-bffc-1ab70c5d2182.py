import os
import json
import csv

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file {} does not exist.".format(file_path))
    except json.JSONDecodeError:
        raise ValueError("Error: The file {} is not a valid JSON file.".format(file_path))

def count_interactions(data, key):
    interactions = {}
    for entry in data:
        value = entry.get(key, "")
        if value in interactions:
            interactions[value] += 1
        else:
            interactions[value] = 1
    return interactions

def main():
    try:
        # Load data from files
        liked_posts_file = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        story_likes_file = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
        reels_comments_file = os.path.join(root_dir, "your_instagram_activity", "comments", "reels_comments.json")

        liked_posts_data = load_json_file(liked_posts_file) if os.path.exists(liked_posts_file) else {"likes_media_likes": []}
        story_likes_data = load_json_file(story_likes_file) if os.path.exists(story_likes_file) else {"story_activities_story_likes": []}
        reels_comments_data = load_json_file(reels_comments_file) if os.path.exists(reels_comments_file) else {"comments_reels_comments": []}

        # Count interactions
        post_likes = count_interactions(liked_posts_data.get("likes_media_likes", []), "title")
        story_likes = count_interactions(story_likes_data.get("story_activities_story_likes", []), "title")
        comments = count_interactions(reels_comments_data.get("comments_reels_comments", []), "string_map_data/Media Owner/value")

        # Combine interactions
        interactions = {}
        for account in set(list(post_likes.keys()) + list(story_likes.keys()) + list(comments.keys())):
            interactions[account] = post_likes.get(account, 0) + story_likes.get(account, 0) + comments.get(account, 0)

        # Get top 20 accounts
        top_accounts = sorted(interactions.items(), key=lambda x: x[1], reverse=True)[:20]

        # Write to CSV file
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
            for account, total_interactions in top_accounts:
                writer.writerow([account, post_likes.get(account, 0), story_likes.get(account, 0), comments.get(account, 0)])

    except Exception as e:
        raise Exception("Error: {}".format(str(e)))

if __name__ == "__main__":
    main()
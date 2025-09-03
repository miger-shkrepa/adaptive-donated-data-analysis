import os
import json
import csv

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        raise ValueError("Error: The file {} is not a valid JSON file.".format(file_path))

def count_interactions(data, key):
    interactions = {}
    for entry in data:
        if key == "Media Owner":
            value = entry.get("string_map_data", {}).get("Media Owner", {}).get("value", "")
        else:
            value = entry.get(key, "")
        if value not in interactions:
            interactions[value] = 1
        else:
            interactions[value] += 1
    return interactions

def main():
    try:
        # Load data from files
        liked_posts_file = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        story_likes_file = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
        reels_comments_file = os.path.join(root_dir, "your_instagram_activity", "comments", "reels_comments.json")

        liked_posts_data = load_json_file(liked_posts_file)
        story_likes_data = load_json_file(story_likes_file)
        reels_comments_data = load_json_file(reels_comments_file)

        # Count interactions
        post_likes = count_interactions(liked_posts_data.get("likes_media_likes", []), "title")
        story_likes = count_interactions(story_likes_data.get("story_activities_story_likes", []), "title")
        comments = count_interactions(reels_comments_data.get("comments_reels_comments", []), "Media Owner")

        # Merge interactions
        interactions = {}
        for account, count in post_likes.items():
            interactions[account] = interactions.get(account, 0) + count
        for account, count in story_likes.items():
            interactions[account] = interactions.get(account, 0) + count
        for account, count in comments.items():
            interactions[account] = interactions.get(account, 0) + count

        # Get top 20 accounts
        top_accounts = sorted(interactions.items(), key=lambda x: x[1], reverse=True)[:20]

        # Write to CSV file
        with open("query_responses/results.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
            for account, count in top_accounts:
                writer.writerow([account, post_likes.get(account, 0), story_likes.get(account, 0), comments.get(account, 0)])

    except ValueError as e:
        print(e)
        with open("query_responses/results.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])

if __name__ == "__main__":
    main()
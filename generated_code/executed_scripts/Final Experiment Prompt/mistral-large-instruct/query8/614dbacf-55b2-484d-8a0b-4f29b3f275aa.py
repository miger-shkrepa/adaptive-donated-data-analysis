import os
import json
import csv

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Warning: File {file_path} does not exist. Skipping this file.")
        return {}
    except json.JSONDecodeError:
        raise ValueError(f"Error: ValueError: The file {file_path} is not a valid JSON.")

def count_interactions(data, key, interaction_type):
    counts = {}
    for item in data.get(key, []):
        title = item.get("title", "")
        if title:
            counts[title] = counts.get(title, 0) + 1
    return counts

def count_comments(data):
    counts = {}
    for item in data.get("comments_reels_comments", []):
        media_owner = item.get("string_map_data", {}).get("Media Owner", {}).get("value", "")
        if media_owner:
            counts[media_owner] = counts.get(media_owner, 0) + 1
    return counts

def main():
    try:
        liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
        reels_comments_path = os.path.join(root_dir, "your_instagram_activity", "comments", "reels_comments.json")

        liked_posts_data = load_json(liked_posts_path)
        story_likes_data = load_json(story_likes_path)
        reels_comments_data = load_json(reels_comments_path)

        post_likes = count_interactions(liked_posts_data, "likes_media_likes", "Post Likes")
        story_likes = count_interactions(story_likes_data, "story_activities_story_likes", "Story Likes")
        comments = count_comments(reels_comments_data)

        all_interactions = {user: (post_likes.get(user, 0), story_likes.get(user, 0), comments.get(user, 0))
                            for user in set(post_likes) | set(story_likes) | set(comments)}

        sorted_interactions = sorted(all_interactions.items(), key=lambda x: sum(x[1]), reverse=True)[:20]

        output_path = "query_responses/results.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["User", "Post Likes", "Story Likes", "Comments"])
            for user, (post_likes, story_likes, comments) in sorted_interactions:
                csvwriter.writerow([user, post_likes, story_likes, comments])

    except Exception as e:
        print(e)
        with open("query_responses/results.csv", 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["User", "Post Likes", "Story Likes", "Comments"])

if __name__ == "__main__":
    main()
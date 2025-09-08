import os
import json
import csv

root_dir = "root_dir"

def load_json(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def count_interactions(data, key):
    interaction_count = {}
    for item in data:
        title = item.get(key, "")
        if title:
            interaction_count[title] = interaction_count.get(title, 0) + 1
    return interaction_count

def count_comments(data):
    interaction_count = {}
    for item in data:
        media_owner = item.get("string_map_data", {}).get("Media Owner", {}).get("value", "")
        if media_owner:
            interaction_count[media_owner] = interaction_count.get(media_owner, 0) + 1
    return interaction_count

def merge_interactions(post_likes, story_likes, comments):
    all_interactions = {}
    for user in post_likes:
        all_interactions[user] = all_interactions.get(user, 0) + post_likes[user]
    for user in story_likes:
        all_interactions[user] = all_interactions.get(user, 0) + story_likes[user]
    for user in comments:
        all_interactions[user] = all_interactions.get(user, 0) + comments[user]
    return all_interactions

def get_top_interactions(interactions, top_n=20):
    sorted_interactions = sorted(interactions.items(), key=lambda x: x[1], reverse=True)
    return sorted_interactions[:top_n]

def main():
    try:
        post_likes_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
        comments_path = os.path.join(root_dir, "your_instagram_activity", "comments", "reels_comments.json")

        post_likes_data = []
        story_likes_data = []
        comments_data = []

        if os.path.exists(post_likes_path):
            post_likes_data = load_json(post_likes_path).get("likes_media_likes", [])
        if os.path.exists(story_likes_path):
            story_likes_data = load_json(story_likes_path).get("story_activities_story_likes", [])
        if os.path.exists(comments_path):
            comments_data = load_json(comments_path).get("comments_reels_comments", [])

        post_likes = count_interactions(post_likes_data, "title")
        story_likes = count_interactions(story_likes_data, "title")
        comments = count_comments(comments_data)

        all_interactions = merge_interactions(post_likes, story_likes, comments)
        top_interactions = get_top_interactions(all_interactions)

        output_path = "query_responses/results.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["User", "Post Likes", "Story Likes", "Comments"])
            for user, total in top_interactions:
                post_likes_count = post_likes.get(user, 0)
                story_likes_count = story_likes.get(user, 0)
                comments_count = comments.get(user, 0)
                csvwriter.writerow([user, post_likes_count, story_likes_count, comments_count])

    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
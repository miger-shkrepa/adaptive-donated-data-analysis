import json
import os
import csv
from collections import defaultdict

def find_file(base_folder, target_file):
    for root, _, files in os.walk(base_folder):
        if target_file in files:
            return os.path.join(root, target_file)
    return None

def extract_interactions(base_folder):
    interactions = defaultdict(lambda: {"Post Likes": 0, "Story Likes": 0, "Comments": 0})

    # Post Likes
    likes_file = find_file(base_folder, "liked_posts.json")
    if likes_file:
        with open(likes_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for entry in data.get("likes_media_likes", []):
                user = entry.get("title")
                if user:
                    interactions[user]["Post Likes"] += 1

    # Story Likes
    story_likes_file = find_file(base_folder, "story_likes.json")
    if story_likes_file:
        with open(story_likes_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for entry in data.get("story_activities_story_likes", []):
                user = entry.get("title")
                if user:
                    interactions[user]["Story Likes"] += 1

    # Comments
    comments_file = find_file(base_folder, "reels_comments.json")
    if comments_file:
        with open(comments_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for entry in data.get("comments_reels_comments", []):
                user = entry.get("string_map_data", {}).get("Media Owner", {}).get("value")
                if user:
                    interactions[user]["Comments"] += 1

    return interactions

def save_top_interactions_to_csv(interactions, output_file):
    try:
        sorted_interactions = sorted(
            interactions.items(),
            key=lambda x: x[1]["Post Likes"] + x[1]["Story Likes"] + x[1]["Comments"],
            reverse=True
        )[:20]

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
            for user, counts in sorted_interactions:
                writer.writerow([user, counts["Post Likes"], counts["Story Likes"], counts["Comments"]])
        print(f"✅ Saved: {output_file}")
    except Exception as e:
        print(f"❌ Error writing CSV: {e}")

def main():
    datasets_dir = "../../datasets"
    output_dir = os.path.join("../../ground_truths", "query8")
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.isdir(datasets_dir):
        print(f"Error: Directory '{datasets_dir}' does not exist.")
        return

    for subdir in os.listdir(datasets_dir):
        full_path = os.path.join(datasets_dir, subdir)
        if not os.path.isdir(full_path):
            continue

        interactions = extract_interactions(full_path)
        if interactions:
            output_file = os.path.join(output_dir, f"{subdir}_ground_truth.csv")
        else:
            output_file = os.path.join(output_dir, f"NODATA_{subdir}_ground_truth.csv")

        save_top_interactions_to_csv(interactions, output_file)

if __name__ == "__main__":
    main()

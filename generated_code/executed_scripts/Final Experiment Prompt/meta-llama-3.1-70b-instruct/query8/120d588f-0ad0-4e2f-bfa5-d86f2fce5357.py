import os
import json
import csv

root_dir = "root_dir"

def get_interactions(root_dir):
    post_likes = {}
    story_likes = {}
    comments = {}

    # Get post likes
    try:
        with open(os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json"), "r") as file:
            data = json.load(file)
            for entry in data["likes_media_likes"]:
                title = entry["title"]
                if title not in post_likes:
                    post_likes[title] = 1
                else:
                    post_likes[title] += 1
    except FileNotFoundError:
        pass

    # Get story likes
    try:
        with open(os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json"), "r") as file:
            data = json.load(file)
            for entry in data["story_activities_story_likes"]:
                title = entry["title"]
                if title not in story_likes:
                    story_likes[title] = 1
                else:
                    story_likes[title] += 1
    except FileNotFoundError:
        pass

    # Get comments
    try:
        with open(os.path.join(root_dir, "your_instagram_activity", "comments", "reels_comments.json"), "r") as file:
            data = json.load(file)
            for entry in data["comments_reels_comments"]:
                media_owner = entry["string_map_data"]["Media Owner"]["value"]
                if media_owner not in comments:
                    comments[media_owner] = 1
                else:
                    comments[media_owner] += 1
    except FileNotFoundError:
        pass

    return post_likes, story_likes, comments

def save_to_csv(post_likes, story_likes, comments):
    with open("query_responses/results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
        users = set(list(post_likes.keys()) + list(story_likes.keys()) + list(comments.keys()))
        for user in sorted(users, key=lambda x: (post_likes.get(x, 0) + story_likes.get(x, 0) + comments.get(x, 0)), reverse=True)[:20]:
            writer.writerow([user, post_likes.get(user, 0), story_likes.get(user, 0), comments.get(user, 0)])

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    post_likes, story_likes, comments = get_interactions(root_dir)
    save_to_csv(post_likes, story_likes, comments)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if not os.path.exists("query_responses"):
            os.makedirs("query_responses")
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
        raise Exception(f"Error: {str(e)}")

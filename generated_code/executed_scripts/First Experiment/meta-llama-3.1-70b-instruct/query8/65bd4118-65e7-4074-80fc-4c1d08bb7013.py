import os
import json
import csv
from collections import defaultdict

root_dir = "root_dir"

def get_interacted_accounts(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize dictionaries to store interaction counts
        post_likes = defaultdict(int)
        story_likes = defaultdict(int)
        comments = defaultdict(int)

        # Iterate over the directory structure
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename == "liked_posts.json":
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        for like in data["likes_media_likes"]:
                            post_likes[like["title"]] += 1
                elif filename == "liked_comments.json":
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        for like in data["likes_comment_likes"]:
                            comments[like["title"]] += 1

        # Get the top 20 interacted accounts
        top_post_likes = sorted(post_likes.items(), key=lambda x: x[1], reverse=True)[:20]
        top_story_likes = sorted(story_likes.items(), key=lambda x: x[1], reverse=True)[:20]
        top_comments = sorted(comments.items(), key=lambda x: x[1], reverse=True)[:20]

        return top_post_likes, top_story_likes, top_comments

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(top_post_likes, top_story_likes, top_comments):
    try:
        # Create the output CSV file
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])

            # Write the top interacted accounts to the CSV file
            for post_like, story_like, comment in zip(top_post_likes, top_story_likes, top_comments):
                writer.writerow([post_like[0], post_like[1], story_like[1], comment[1]])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        top_post_likes, top_story_likes, top_comments = get_interacted_accounts(root_dir)
        save_to_csv(top_post_likes, top_story_likes, top_comments)
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()
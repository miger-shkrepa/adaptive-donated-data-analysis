import os
import csv
import json

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

def get_likes_data(root_dir):
    likes_data = {}
    try:
        liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        liked_comments_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_comments.json")

        if os.path.exists(liked_posts_path):
            liked_posts_data = load_json_file(liked_posts_path)
            for like in liked_posts_data.get("likes_media_likes", []):
                for item in like.get("string_list_data", []):
                    user = item.get("value")
                    if user:
                        likes_data[user] = likes_data.get(user, 0) + 1

        if os.path.exists(liked_comments_path):
            liked_comments_data = load_json_file(liked_comments_path)
            for like in liked_comments_data.get("likes_comment_likes", []):
                for item in like.get("string_list_data", []):
                    user = item.get("value")
                    if user:
                        likes_data[user] = likes_data.get(user, 0) + 1

    except Exception as e:
        print(f"Error processing likes data: {e}")

    return likes_data

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    likes_data = get_likes_data(root_dir)

    # Sort the likes data by the number of interactions in descending order
    sorted_likes = sorted(likes_data.items(), key=lambda x: x[1], reverse=True)

    # Get the top 20 interactions
    top_20_interactions = sorted_likes[:20]

    # Prepare the CSV file
    csv_file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["User", "Post Likes", "Story Likes and Comments"])
        for user, count in top_20_interactions:
            writer.writerow([user, count, 0])  # Assuming all likes are either post likes or story likes and comments

if __name__ == "__main__":
    main()
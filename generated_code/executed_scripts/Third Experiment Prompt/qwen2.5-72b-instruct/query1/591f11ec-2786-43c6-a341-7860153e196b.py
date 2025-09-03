import os
import json
import csv

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    topics = set()

    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        likes_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        saved_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")

        if os.path.exists(likes_path):
            with open(likes_path, 'r') as likes_file:
                likes_data = json.load(likes_file)
                for item in likes_data.get("likes_media_likes", []):
                    title = item.get("title")
                    if title:
                        topics.add(title)

        if os.path.exists(saved_path):
            with open(saved_path, 'r') as saved_file:
                saved_data = json.load(saved_file)
                for item in saved_data.get("saved_saved_media", []):
                    title = item.get("title")
                    if title:
                        topics.add(title)

    except FileNotFoundError as e:
        print(e)
    except json.JSONDecodeError as e:
        print(f"Error: JSON decoding error - {e}")
    except Exception as e:
        print(f"Error: Unexpected error - {e}")

    return topics

def write_topics_to_csv(topics):
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Topics of Interest"])
        for topic in topics:
            writer.writerow([topic])

if __name__ == "__main__":
    try:
        topics_of_interest = get_topics_of_interest(root_dir)
        write_topics_to_csv(topics_of_interest)
    except Exception as e:
        print(f"Error: {e}")
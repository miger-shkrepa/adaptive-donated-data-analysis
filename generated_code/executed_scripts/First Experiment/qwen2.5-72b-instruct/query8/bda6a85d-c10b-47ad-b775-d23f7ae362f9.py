import os
import json
import csv
from collections import Counter

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The JSON file is not properly formatted.")

def get_interactions():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")

        post_likes = Counter()
        story_likes = Counter()
        comments = Counter()

        for dirpath, _, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename == "liked_posts.json":
                    liked_posts = load_json(os.path.join(dirpath, filename))
                    for post in liked_posts["likes_media_likes"]:
                        for like in post["string_list_data"]:
                            post_likes[like["value"]] += 1

                if filename == "instagram_profile_information.json":
                    profile_info = load_json(os.path.join(dirpath, filename))
                    for insight in profile_info["profile_account_insights"]:
                        for key, value in insight["string_map_data"].items():
                            if "Story" in key and "Time" in key:
                                story_likes[value["value"]] += 1

                if "message_1.json" in filename and "inbox" in dirpath:
                    messages = load_json(os.path.join(dirpath, filename))
                    for message in messages["messages"]:
                        if "content" in message:
                            comments[message["sender_name"]] += 1

        interactions = Counter()
        for counter in [post_likes, story_likes, comments]:
            interactions.update(counter)

        return interactions.most_common(20)

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def write_to_csv(interactions):
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for user, count in interactions:
            writer.writerow({
                'User': user,
                'Post Likes': post_likes[user],
                'Story Likes': story_likes[user],
                'Comments': comments[user]
            })

if __name__ == "__main__":
    try:
        interactions = get_interactions()
        write_to_csv(interactions)
    except Exception as e:
        print(e)
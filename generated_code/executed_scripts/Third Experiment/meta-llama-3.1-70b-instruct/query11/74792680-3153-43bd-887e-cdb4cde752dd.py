import os
import csv

root_dir = "root_dir"

def get_viewed_posts(root_dir):
    try:
        viewed_posts = set()
        story_interactions_dir = os.path.join(root_dir, "story_interactions")
        if os.path.exists(story_interactions_dir):
            emoji_story_reactions_file = os.path.join(story_interactions_dir, "emoji_story_reactions.json")
            if os.path.exists(emoji_story_reactions_file):
                with open(emoji_story_reactions_file, 'r') as file:
                    # Assuming the JSON file has the same structure as the provided context
                    import json
                    data = json.load(file)
                    for item in data["story_activities_emoji_quick_reactions"]:
                        for post in item["string_list_data"]:
                            viewed_posts.add(post["value"])
        return viewed_posts
    except Exception as e:
        raise ValueError("Error: Failed to retrieve viewed posts: " + str(e))

def get_liked_posts(root_dir):
    try:
        liked_posts = set()
        saved_posts_file = os.path.join(root_dir, "saved_posts.json")
        if os.path.exists(saved_posts_file):
            with open(saved_posts_file, 'r') as file:
                import json
                data = json.load(file)
                for item in data["saved_saved_media"]:
                    liked_posts.add(item["title"])
        return liked_posts
    except Exception as e:
        raise ValueError("Error: Failed to retrieve liked posts: " + str(e))

def get_accounts(root_dir):
    try:
        accounts = set()
        media_dir = os.path.join(root_dir, "media")
        if os.path.exists(media_dir):
            posts_dir = os.path.join(media_dir, "posts")
            if os.path.exists(posts_dir):
                for filename in os.listdir(posts_dir):
                    if filename.endswith(".mp4") or filename.endswith(".srt"):
                        accounts.add(filename.split("_")[0])
        return accounts
    except Exception as e:
        raise ValueError("Error: Failed to retrieve accounts: " + str(e))

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        viewed_posts = get_viewed_posts(root_dir)
        liked_posts = get_liked_posts(root_dir)
        accounts = get_accounts(root_dir)
        
        result = []
        for account in accounts:
            if account in viewed_posts and account not in liked_posts:
                result.append([account])
        
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Account"])
            writer.writerows(result)
    except Exception as e:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Account"])
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()
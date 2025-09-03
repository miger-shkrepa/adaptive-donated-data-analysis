import os
import json
import csv

root_dir = "root_dir"

def get_interacted_accounts(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize dictionaries to store interaction counts
        post_likes = {}
        story_likes = {}
        comments = {}

        # Iterate over messages directory
        messages_dir = os.path.join(root_dir, "messages", "inbox")
        if os.path.exists(messages_dir):
            for filename in os.listdir(messages_dir):
                if filename.endswith(".json"):
                    file_path = os.path.join(messages_dir, filename)
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        for message in data.get("messages", []):
                            sender_name = message.get("sender_name")
                            if sender_name:
                                if "reactions" in message:
                                    reaction = message["reactions"][0].get("reaction")
                                    if reaction == "Like":
                                        post_likes[sender_name] = post_likes.get(sender_name, 0) + 1
                                if "share" in message:
                                    story_likes[sender_name] = story_likes.get(sender_name, 0) + 1
                                if "content" in message:
                                    comments[sender_name] = comments.get(sender_name, 0) + 1

        # Get top 20 interacted accounts
        top_accounts = sorted(set(list(post_likes.keys()) + list(story_likes.keys()) + list(comments.keys())), key=lambda x: (post_likes.get(x, 0), story_likes.get(x, 0), comments.get(x, 0)), reverse=True)[:20]

        # Create CSV data
        csv_data = []
        for account in top_accounts:
            csv_data.append({
                "User": account,
                "Post Likes": post_likes.get(account, 0),
                "Story Likes": story_likes.get(account, 0),
                "Comments": comments.get(account, 0)
            })

        return csv_data

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(csv_data, filename):
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["User", "Post Likes", "Story Likes", "Comments"])
            writer.writeheader()
            writer.writerows(csv_data)
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        csv_data = get_interacted_accounts(root_dir)
        if not csv_data:
            csv_data = [{"User": "", "Post Likes": "", "Story Likes": "", "Comments": ""}]
        save_to_csv(csv_data, "query_responses/results.csv")
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()
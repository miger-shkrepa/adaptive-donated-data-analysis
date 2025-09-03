import os
import json
import csv

root_dir = "root_dir"

def get_story_engagements(root_dir):
    story_engagements = {}
    try:
        messages_dir = os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")
        if not os.path.exists(messages_dir):
            return story_engagements
        for username in os.listdir(messages_dir):
            user_dir = os.path.join(messages_dir, username)
            for filename in os.listdir(user_dir):
                if filename.startswith("message_") and filename.endswith(".json"):
                    file_path = os.path.join(user_dir, filename)
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        for message in data["messages"]:
                            if "share" in message and "original_content_owner" in message["share"]:
                                story_owner = message["share"]["original_content_owner"]
                                if story_owner not in story_engagements:
                                    story_engagements[story_owner] = 1
                                else:
                                    story_engagements[story_owner] += 1
    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory does not exist.")
    except Exception as e:
        raise ValueError("Error: " + str(e))
    return story_engagements

def write_to_csv(story_engagements):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["User", "Times Engaged"])
        for user, engagements in story_engagements.items():
            writer.writerow([user, engagements])

def main():
    try:
        story_engagements = get_story_engagements(root_dir)
        write_to_csv(story_engagements)
    except Exception as e:
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["User", "Times Engaged"])
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()
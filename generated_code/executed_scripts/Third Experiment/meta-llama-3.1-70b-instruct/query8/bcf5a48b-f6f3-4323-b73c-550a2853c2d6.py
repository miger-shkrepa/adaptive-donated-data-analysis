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

        # Iterate over files in root directory
        for filename in os.listdir(root_dir):
            filepath = os.path.join(root_dir, filename)

            # Check if file is a JSON file
            if filename.endswith(".json"):
                with open(filepath, 'r') as file:
                    data = json.load(file)

                    # Check if file contains post likes data
                    if filename == "story_likes.json":
                        for item in data["story_activities_story_likes"]:
                            for like in item["string_list_data"]:
                                user = item["title"]
                                if user not in story_likes:
                                    story_likes[user] = 1
                                else:
                                    story_likes[user] += 1

                    # Check if file contains story likes data
                    elif filename == "story_likes.json":
                        for item in data["story_activities_story_likes"]:
                            for like in item["string_list_data"]:
                                user = item["title"]
                                if user not in story_likes:
                                    story_likes[user] = 1
                                else:
                                    story_likes[user] += 1

                    # Check if file contains comments data
                    elif filename == "questions.json":
                        for item in data["story_activities_questions"]:
                            for comment in item["string_list_data"]:
                                user = item["title"]
                                if user not in comments:
                                    comments[user] = 1
                                else:
                                    comments[user] += 1

                    # Check if file contains post likes data
                    elif filename == "quizzes.json":
                        for item in data["story_activities_quizzes"]:
                            for like in item["string_list_data"]:
                                user = item["title"]
                                if user not in post_likes:
                                    post_likes[user] = 1
                                else:
                                    post_likes[user] += 1

        # Combine interaction counts
        interacted_accounts = {}
        for user in set(list(post_likes.keys()) + list(story_likes.keys()) + list(comments.keys())):
            interacted_accounts[user] = post_likes.get(user, 0) + story_likes.get(user, 0) + comments.get(user, 0)

        # Get top 20 interacted accounts
        top_accounts = sorted(interacted_accounts.items(), key=lambda x: x[1], reverse=True)[:20]

        return top_accounts

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(accounts):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
            for account in accounts:
                writer.writerow([account[0], 0, 0, account[1]])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        accounts = get_interacted_accounts(root_dir)
        save_to_csv(accounts)

    except Exception as e:
        print("Error: " + str(e))
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])

if __name__ == "__main__":
    main()
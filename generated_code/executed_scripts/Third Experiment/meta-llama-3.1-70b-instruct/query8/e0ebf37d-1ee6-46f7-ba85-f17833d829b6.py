import os
import json
import csv

root_dir = "root_dir"

def get_interacted_accounts(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        interacted_accounts = {}

        # Iterate over all files in the directory
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith(".json"):
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)

                        # Check if the file contains messages
                        if 'messages' in data:
                            for message in data['messages']:
                                if 'sender_name' in message:
                                    sender_name = message['sender_name']
                                    if sender_name not in interacted_accounts:
                                        interacted_accounts[sender_name] = {'post_likes': 0, 'story_likes': 0, 'comments': 0}

                                    # Check if the message contains a share
                                    if 'share' in message:
                                        interacted_accounts[sender_name]['post_likes'] += 1
                                    else:
                                        interacted_accounts[sender_name]['comments'] += 1

                        # Check if the file contains story likes
                        if 'story_likes' in data:
                            for story_like in data['story_likes']:
                                if 'sender_name' in story_like:
                                    sender_name = story_like['sender_name']
                                    if sender_name not in interacted_accounts:
                                        interacted_accounts[sender_name] = {'post_likes': 0, 'story_likes': 0, 'comments': 0}
                                    interacted_accounts[sender_name]['story_likes'] += 1

        # Sort interacted accounts by total interactions
        sorted_accounts = sorted(interacted_accounts.items(), key=lambda x: sum(x[1].values()), reverse=True)

        return sorted_accounts[:20]

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(accounts):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
            for account, interactions in accounts:
                writer.writerow([account, interactions['post_likes'], interactions['story_likes'], interactions['comments']])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        accounts = get_interacted_accounts(root_dir)
        if not accounts:
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
        else:
            save_to_csv(accounts)

    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()
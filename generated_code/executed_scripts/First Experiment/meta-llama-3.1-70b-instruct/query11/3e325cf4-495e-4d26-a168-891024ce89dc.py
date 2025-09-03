import os
import json
import csv

root_dir = "root_dir"

def get_viewed_but_not_liked_accounts(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        viewed_accounts = set()
        liked_accounts = set()

        # Iterate over all files in the directory
        for dir_path, dir_names, file_names in os.walk(root_dir):
            for file_name in file_names:
                if file_name == "event_reminders.json":
                    file_path = os.path.join(dir_path, file_name)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        for event in data["events_event_reminders"]:
                            for string_data in event["string_list_data"]:
                                viewed_accounts.add(string_data["value"])

                elif file_name == "liked_posts.json":
                    file_path = os.path.join(dir_path, file_name)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        for like in data["likes_media_likes"]:
                            for string_data in like["string_list_data"]:
                                liked_accounts.add(string_data["value"])

        # Find accounts that have been viewed but not liked
        viewed_but_not_liked_accounts = viewed_accounts - liked_accounts

        return viewed_but_not_liked_accounts

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(accounts, csv_file_path):
    try:
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Account"])
            for account in accounts:
                csv_writer.writerow([account])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        viewed_but_not_liked_accounts = get_viewed_but_not_liked_accounts(root_dir)
        csv_file_path = 'query_responses/results.csv'
        save_to_csv(viewed_but_not_liked_accounts, csv_file_path)

    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()
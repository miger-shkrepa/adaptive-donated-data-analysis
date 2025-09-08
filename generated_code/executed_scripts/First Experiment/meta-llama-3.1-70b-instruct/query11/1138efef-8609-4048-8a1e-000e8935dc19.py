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
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                # Check if the file is a JSON file
                if filename.endswith(".json"):
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, "r") as file:
                        data = json.load(file)

                        # Check if the file contains viewed posts
                        if "media" in data and "title" in data:
                            for post in data["media"]:
                                if "uri" in post:
                                    viewed_accounts.add(post["uri"].split("/")[-1])

                        # Check if the file contains liked posts
                        if "likes_media_likes" in data:
                            for like in data["likes_media_likes"]:
                                if "string_list_data" in like:
                                    for item in like["string_list_data"]:
                                        if "href" in item:
                                            liked_accounts.add(item["href"].split("/")[-1])

        # Find accounts that have been viewed but not liked
        viewed_but_not_liked = viewed_accounts - liked_accounts

        return viewed_but_not_liked

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(accounts, filename):
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Account"])
            for account in accounts:
                writer.writerow([account])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        accounts = get_viewed_but_not_liked_accounts(root_dir)
        save_to_csv(accounts, "query_responses/results.csv")

    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()
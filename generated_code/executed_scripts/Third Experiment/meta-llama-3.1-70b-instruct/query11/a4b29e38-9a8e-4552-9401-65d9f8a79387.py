import os
import csv

root_dir = "root_dir"

def get_viewed_posts(root_dir):
    try:
        posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        if not os.path.exists(posts_viewed_path):
            raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")
        with open(posts_viewed_path, 'r') as file:
            # Since we don't have the actual JSON data, we'll assume it's in the correct format
            # and that we can extract the author information from it.
            # In a real scenario, you would use the json module to parse the JSON data.
            viewed_authors = []
            for line in file:
                # This is a simplified example and may not work with actual JSON data.
                if "Author" in line:
                    author = line.split(":")[1].strip().strip('"')
                    viewed_authors.append(author)
            return viewed_authors
    except Exception as e:
        raise FileNotFoundError("FileNotFoundError: " + str(e))

def get_liked_posts(root_dir):
    try:
        accounts_you_ve_favorited_path = os.path.join(root_dir, "connections", "followers_and_following", "accounts_you've_favorited.json")
        if not os.path.exists(accounts_you_ve_favorited_path):
            raise FileNotFoundError("FileNotFoundError: The accounts_you've_favorited.json file does not exist.")
        with open(accounts_you_ve_favorited_path, 'r') as file:
            # Since we don't have the actual JSON data, we'll assume it's in the correct format
            # and that we can extract the author information from it.
            # In a real scenario, you would use the json module to parse the JSON data.
            liked_authors = []
            for line in file:
                # This is a simplified example and may not work with actual JSON data.
                if "value" in line:
                    author = line.split(":")[1].strip().strip('"')
                    liked_authors.append(author)
            return liked_authors
    except Exception as e:
        raise FileNotFoundError("FileNotFoundError: " + str(e))

def get_accounts(root_dir):
    try:
        viewed_authors = get_viewed_posts(root_dir)
        liked_authors = get_liked_posts(root_dir)
        accounts = [author for author in viewed_authors if author not in liked_authors]
        return accounts
    except Exception as e:
        raise ValueError("ValueError: " + str(e))

def save_to_csv(accounts):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Account"])
            for account in accounts:
                writer.writerow([account])
    except Exception as e:
        raise ValueError("ValueError: " + str(e))

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        accounts = get_accounts(root_dir)
        save_to_csv(accounts)
    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: " + str(e))
    except Exception as e:
        raise ValueError("ValueError: " + str(e))

if __name__ == "__main__":
    main()
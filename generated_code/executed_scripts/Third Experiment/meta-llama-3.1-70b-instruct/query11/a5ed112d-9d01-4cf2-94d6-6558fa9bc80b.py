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
            # and extract the authors
            viewed_authors = []
            for line in file:
                if "Author" in line:
                    author = line.split(":")[1].strip().replace('"', '')
                    viewed_authors.append(author)
        return viewed_authors
    except Exception as e:
        raise FileNotFoundError("Error: " + str(e))

def get_liked_posts(root_dir):
    try:
        liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        if not os.path.exists(liked_posts_path):
            raise FileNotFoundError("FileNotFoundError: The liked_posts.json file does not exist.")
        with open(liked_posts_path, 'r') as file:
            # Since we don't have the actual JSON data, we'll assume it's in the correct format
            # and extract the authors
            liked_authors = []
            for line in file:
                if "value" in line:
                    author = line.split(":")[1].strip().replace('"', '')
                    liked_authors.append(author)
        return liked_authors
    except Exception as e:
        raise FileNotFoundError("Error: " + str(e))

def get_accounts(root_dir):
    try:
        viewed_authors = get_viewed_posts(root_dir)
        liked_authors = get_liked_posts(root_dir)
        accounts = [author for author in viewed_authors if author not in liked_authors]
        return accounts
    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(accounts):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Account"])
            for account in accounts:
                writer.writerow([account])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        accounts = get_accounts(root_dir)
        save_to_csv(accounts)
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Account"])
        raise FileNotFoundError("Error: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()
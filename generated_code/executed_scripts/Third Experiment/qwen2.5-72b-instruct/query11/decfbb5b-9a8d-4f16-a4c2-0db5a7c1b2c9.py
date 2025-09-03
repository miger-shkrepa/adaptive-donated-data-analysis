import os
import json
import csv

root_dir = "root_dir"

def get_viewed_authors(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            authors = set()
            for entry in data.get("impressions_history_posts_seen", []):
                author = entry.get("string_map_data", {}).get("Author", {}).get("value")
                if author:
                    authors.add(author)
            return authors
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def get_liked_authors(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            authors = set()
            for entry in data.get("impressions_history_posts_seen", []):
                author = entry.get("string_map_data", {}).get("Author", {}).get("value")
                if author and entry.get("string_map_data", {}).get("Liked", {}).get("value") == "True":
                    authors.add(author)
            return authors
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def find_accounts_viewed_not_liked(root_dir):
    try:
        viewed_authors_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        liked_authors_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_liked.json")

        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        viewed_authors = get_viewed_authors(viewed_authors_file) if os.path.exists(viewed_authors_file) else set()
        liked_authors = get_liked_authors(liked_authors_file) if os.path.exists(liked_authors_file) else set()

        accounts_viewed_not_liked = viewed_authors - liked_authors

        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for account in accounts_viewed_not_liked:
                writer.writerow([account])

    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(e)

find_accounts_viewed_not_liked(root_dir)
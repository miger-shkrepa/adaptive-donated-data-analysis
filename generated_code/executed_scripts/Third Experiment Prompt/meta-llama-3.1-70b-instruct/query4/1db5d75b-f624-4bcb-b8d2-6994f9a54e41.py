import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access(root_dir):
    companies = set()
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Check if 'your_instagram_activity' directory exists
        activity_dir = os.path.join(root_dir, "your_instagram_activity")
        if not os.path.exists(activity_dir):
            return companies

        # Check if 'likes' and 'saved' directories exist
        likes_dir = os.path.join(activity_dir, "likes")
        saved_dir = os.path.join(activity_dir, "saved")
        if not os.path.exists(likes_dir) or not os.path.exists(saved_dir):
            return companies

        # Parse 'liked_posts.json' and 'saved_posts.json' files
        liked_posts_file = os.path.join(likes_dir, "liked_posts.json")
        saved_posts_file = os.path.join(saved_dir, "saved_posts.json")
        if os.path.exists(liked_posts_file):
            with open(liked_posts_file, "r") as f:
                liked_posts_data = json.load(f)
                for post in liked_posts_data["likes_media_likes"]:
                    companies.add(post["title"])
        if os.path.exists(saved_posts_file):
            with open(saved_posts_file, "r") as f:
                saved_posts_data = json.load(f)
                for post in saved_posts_data["saved_saved_media"]:
                    companies.add(post["title"])

        return companies

    except json.JSONDecodeError as e:
        raise ValueError("Error: Invalid JSON format in file: {}".format(e))
    except Exception as e:
        raise Exception("Error: {}".format(e))

def write_companies_to_csv(companies):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name"])  # header
        for company in companies:
            writer.writerow([company])

companies = get_companies_with_access(root_dir)
write_companies_to_csv(companies)
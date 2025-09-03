import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Function to extract viewed posts
def extract_viewed_posts(root_dir):
    viewed_posts = set()
    try:
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith("posts_1.json"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        for post in data.get("media", []):
                            viewed_posts.add(post.get("title"))
    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON.")
    return viewed_posts

# Function to extract liked posts
def extract_liked_posts(root_dir):
    liked_posts = set()
    try:
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith("liked_posts.json"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        for post in data.get("likes_media_likes", []):
                            liked_posts.add(post.get("title"))
    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON.")
    return liked_posts

# Main function to find accounts viewed but not liked
def find_viewed_but_not_liked(root_dir):
    viewed_posts = extract_viewed_posts(root_dir)
    liked_posts = extract_liked_posts(root_dir)
    viewed_but_not_liked = viewed_posts - liked_posts

    # Write the results to a CSV file
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account"])
        for account in viewed_but_not_liked:
            writer.writerow([account])

# Execute the main function
find_viewed_but_not_liked(root_dir)
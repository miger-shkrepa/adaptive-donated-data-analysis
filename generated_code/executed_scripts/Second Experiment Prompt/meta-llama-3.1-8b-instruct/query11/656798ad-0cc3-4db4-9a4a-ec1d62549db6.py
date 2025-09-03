import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

try:
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
except FileNotFoundError as e:
    print(e)
    exit(1)

# Initialize the result list
results = []

# Iterate over the JSON files in the 'your_instagram_activity/likes' directory
likes_dir = os.path.join(root_dir, "your_instagram_activity", "likes")
for filename in os.listdir(likes_dir):
    if filename.endswith(".json"):
        # Load the JSON file
        with open(os.path.join(likes_dir, filename), "r") as f:
            data = json.load(f)
        
        # Check if the 'structure' key exists in the JSON file
        if "structure" in data:
            # Extract the 'likes_media_likes' list
            likes_media_likes = data["structure"]["likes_media_likes"]
            
            # Iterate over the 'likes_media_likes' list
            for liked_post in likes_media_likes:
                # Extract the 'title' and 'href' of the liked post
                title = liked_post["title"]
                href = liked_post["string_list_data"][0]["href"]
                
                # Check if the post is in the 'saved_saved_media' list
                saved_dir = os.path.join(root_dir, "your_instagram_activity", "saved")
                saved_filename = "saved_posts.json"
                saved_file_path = os.path.join(saved_dir, saved_filename)
                if os.path.exists(saved_file_path):
                    with open(saved_file_path, "r") as f:
                        saved_data = json.load(f)
                    if "structure" in saved_data:
                        saved_saved_media = saved_data["structure"]["saved_saved_media"]
                        post_in_saved = False
                        for saved_post in saved_saved_media:
                            if saved_post["title"] == title and saved_post["string_map_data"]["Saved on"]["href"] == href:
                                post_in_saved = True
                                break
                        # If the post is not in the 'saved_saved_media' list, add it to the results
                        if not post_in_saved:
                            results.append(title)
                else:
                    # If the 'saved_posts.json' file does not exist, treat its contribution as 0
                    results.append(title)
        else:
            # If the 'structure' key does not exist in the JSON file, treat its contribution as 0
            results.append(filename)

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account"])  # Write the header
    for result in results:
        writer.writerow([result])
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
        
        # Check if the 'structure' key exists
        if "structure" in data:
            # Extract the 'likes_media_likes' list
            likes_media_likes = data["structure"].get("likes_media_likes", [])
            
            # Iterate over the 'saved_saved_media' list in the 'saved_posts.json' file
            saved_dir = os.path.join(root_dir, "your_instagram_activity", "saved")
            for saved_filename in os.listdir(saved_dir):
                if saved_filename.endswith(".json"):
                    # Load the JSON file
                    with open(os.path.join(saved_dir, saved_filename), "r") as f:
                        saved_data = json.load(f)
                    
                    # Check if the 'structure' key exists
                    if "structure" in saved_data:
                        # Extract the 'saved_saved_media' list
                        saved_saved_media = saved_data["structure"].get("saved_saved_media", [])
                        
                        # Iterate over the 'saved_saved_media' list
                        for saved_post in saved_saved_media:
                            # Check if the post is in the 'likes_media_likes' list
                            if any(post["title"] == saved_post["title"] for post in likes_media_likes):
                                # If the post is in the 'likes_media_likes' list, skip it
                                continue
                            
                            # Add the account to the result list
                            results.append(saved_post["title"])

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account"])  # Write the header
    writer.writerows(results)
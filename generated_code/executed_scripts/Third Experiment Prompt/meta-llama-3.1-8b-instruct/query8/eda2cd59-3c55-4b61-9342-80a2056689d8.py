import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

try:
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
except Exception as e:
    print(f"Error: {e}")
    exit(1)

# Initialize the result dictionary
result = {"User": [], "Post Likes": [], "Story Likes": [], "Comments": []}

# Initialize counters for post likes, story likes and comments
post_likes_count = 0
story_likes_count = 0
comments_count = 0

# Iterate over the 'likes' and 'saved' directories
for dir_name in ["likes", "saved"]:
    dir_path = os.path.join(root_dir, "your_instagram_activity", dir_name)
    if os.path.exists(dir_path):
        # Iterate over the JSON files in the directory
        for file_name in os.listdir(dir_path):
            if file_name.endswith(".json"):
                file_path = os.path.join(dir_path, file_name)
                try:
                    # Load the JSON file
                    with open(file_path, "r") as f:
                        data = json.load(f)
                    # Extract the relevant data
                    if dir_name == "likes":
                        if "structure" in data and "likes_media_likes" in data["structure"]:
                            for item in data["structure"]["likes_media_likes"]:
                                user = item["title"]
                                post_likes = len(item["string_list_data"])
                                story_likes = 0
                                comments = 0
                                result["User"].append(user)
                                result["Post Likes"].append(post_likes)
                                result["Story Likes"].append(story_likes)
                                result["Comments"].append(comments)
                                post_likes_count += 1
                        else:
                            print(f"Warning: Missing key 'structure' or 'likes_media_likes' in JSON file {file_path}. Treating its contribution as 0.")
                    elif dir_name == "saved":
                        if "structure" in data and "saved_saved_media" in data["structure"]:
                            for item in data["structure"]["saved_saved_media"]:
                                user = item["title"]
                                post_likes = 0
                                story_likes = 0
                                comments = len(item["string_map_data"])
                                result["User"].append(user)
                                result["Post Likes"].append(post_likes)
                                result["Story Likes"].append(story_likes)
                                result["Comments"].append(comments)
                                comments_count += 1
                        else:
                            print(f"Warning: Missing key 'structure' or 'saved_saved_media' in JSON file {file_path}. Treating its contribution as 0.")
                except json.JSONDecodeError:
                    print(f"Error: Failed to parse JSON file {file_path}")
                except KeyError as e:
                    print(f"Error: Missing key '{e}' in JSON file {file_path}")
                except Exception as e:
                    print(f"Error: {e}")
    else:
        # If the directory does not exist, treat its contribution as 0
        for i in range(20):
            result["User"].append("")
            result["Post Likes"].append(0)
            result["Story Likes"].append(0)
            result["Comments"].append(0)

# Sort the result by Post Likes in descending order
result["User"] = [x for _, x in sorted(zip(result["Post Likes"], result["User"]), reverse=True)]
result["Post Likes"] = sorted(result["Post Likes"], reverse=True)
result["Story Likes"] = [0] * min(20, post_likes_count)
result["Comments"] = [0] * min(20, comments_count)

# Save the result to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for i in range(min(20, post_likes_count)):
        writer.writerow([result["User"][i], result["Post Likes"][i], result["Story Likes"][i], result["Comments"][i]])
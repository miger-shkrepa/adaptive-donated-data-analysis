import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the data structures
post_likes = {}
story_likes = {}
comments = {}

# Iterate over the JSON files
for filename in os.listdir(root_dir):
    if filename.endswith(".json"):
        filepath = os.path.join(root_dir, filename)
        with open(filepath, 'r') as file:
            data = eval(file.read())
            for key, value in data.items():
                if key == "story_likes.json":
                    for item in value["structure"]["story_activities_story_likes"]:
                        for string in item["string_list_data"]:
                            if "timestamp" in string:
                                timestamp = string["timestamp"]
                                if timestamp not in story_likes:
                                    story_likes[timestamp] = 1
                                else:
                                    story_likes[timestamp] += 1
                elif key == "reels.json":
                    for item in value["structure"]["subscriptions_reels"]:
                        for string in item["string_map_data"].values():
                            if "timestamp" in string:
                                timestamp = string["timestamp"]
                                if timestamp not in post_likes:
                                    post_likes[timestamp] = 1
                                else:
                                    post_likes[timestamp] += 1
                elif key == "recently_unfollowed_accounts.json":
                    for item in value["structure"]["relationships_unfollowed_users"]:
                        for string in item["string_list_data"]:
                            if "timestamp" in string:
                                timestamp = string["timestamp"]
                                if timestamp not in comments:
                                    comments[timestamp] = 1
                                else:
                                    comments[timestamp] += 1

# Sort the data by timestamp and get the top 20
top_20_post_likes = sorted(post_likes.items(), key=lambda x: x[1], reverse=True)[:20]
top_20_story_likes = sorted(story_likes.items(), key=lambda x: x[1], reverse=True)[:20]
top_20_comments = sorted(comments.items(), key=lambda x: x[1], reverse=True)[:20]

# Create the CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for i in range(max(len(top_20_post_likes), len(top_20_story_likes), len(top_20_comments))):
        user = f"User {i+1}"
        post_like = top_20_post_likes[i][1] if i < len(top_20_post_likes) else 0
        story_like = top_20_story_likes[i][1] if i < len(top_20_story_likes) else 0
        comment = top_20_comments[i][1] if i < len(top_20_comments) else 0
        writer.writerow([user, post_like, story_like, comment])
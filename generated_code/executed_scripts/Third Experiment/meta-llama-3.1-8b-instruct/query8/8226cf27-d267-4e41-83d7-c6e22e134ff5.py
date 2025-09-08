import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the dictionaries to store the interactions
post_likes = {}
story_likes = {}
comments = {}

# Function to process the JSON files
def process_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            # Assuming the JSON data is in the format of a Python dictionary
            json_data = eval(data)
            # Process the JSON data
            for key, value in json_data.items():
                if key == "likes":
                    for file_name, file_data in value.items():
                        if file_name == "liked_posts.json":
                            for post in file_data["structure"]["likes_media_likes"]:
                                post_title = post["title"]
                                if post_title in post_likes:
                                    post_likes[post_title] += 1
                                else:
                                    post_likes[post_title] = 1
                elif key == "events":
                    for file_name, file_data in value.items():
                        if file_name == "event_reminders.json":
                            for event in file_data["structure"]["events_event_reminders"]:
                                event_title = event["title"]
                                if event_title in story_likes:
                                    story_likes[event_title] += 1
                                else:
                                    story_likes[event_title] = 1
                elif key == "messages":
                    for file_name, file_data in value.items():
                        if file_name == "inbox":
                            for message in file_data["structure"]["message_1.json"]["structure"]["messages"]:
                                sender_name = message["sender_name"]
                                if sender_name in comments:
                                    comments[sender_name] += 1
                                else:
                                    comments[sender_name] = 1
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")

# Function to process the directory structure
def process_directory_structure(root_dir):
    try:
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith(".json"):
                    process_json_file(file_path)
    except Exception as e:
        print(f"Error processing directory structure: {str(e)}")

# Process the directory structure
process_directory_structure(root_dir)

# Create the CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for user in post_likes:
        post_likes[user] = post_likes[user] if user in story_likes else 0
        post_likes[user] = post_likes[user] if user in comments else 0
        writer.writerow([user, post_likes[user], story_likes.get(user, 0), comments.get(user, 0)])

# Print the top 20 users
top_users = sorted(post_likes.items(), key=lambda x: x[1], reverse=True)[:20]
for user, likes in top_users:
    print(f"{user}: {likes}")
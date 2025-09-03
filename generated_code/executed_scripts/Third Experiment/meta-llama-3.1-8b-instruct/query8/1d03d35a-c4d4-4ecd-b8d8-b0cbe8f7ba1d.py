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
            # Assuming the JSON data is in the format of a list of dictionaries
            for item in eval(data):
                if 'posts_viewed.json' in file_path:
                    for post in item['impressions_history_posts_seen']:
                        author = post['string_map_data']['Author']['value']
                        if author not in post_likes:
                            post_likes[author] = 0
                        post_likes[author] += 1
                elif 'videos_watched.json' in file_path:
                    for video in item['impressions_history_videos_watched']:
                        author = video['string_map_data']['Author']['value']
                        if author not in post_likes:
                            post_likes[author] = 0
                        post_likes[author] += 1
                elif 'accounts_you\'ve_favorited.json' in file_path:
                    for favorite in item['relationships_feed_favorites']:
                        author = favorite['title']
                        if author not in story_likes:
                            story_likes[author] = 0
                        story_likes[author] += 1
                elif 'close_friends.json' in file_path:
                    for friend in item['relationships_close_friends']:
                        author = friend['title']
                        if author not in story_likes:
                            story_likes[author] = 0
                        story_likes[author] += 1
                elif 'followers_1.json' in file_path:
                    for follower in item['relationships_following']:
                        author = follower['title']
                        if author not in comments:
                            comments[author] = 0
                        comments[author] += 1
                elif 'following.json' in file_path:
                    for following in item['relationships_follow_requests_received']:
                        author = following['title']
                        if author not in comments:
                            comments[author] = 0
                        comments[author] += 1
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")

# Function to process the directory
def process_directory(directory):
    try:
        for item in os.listdir(directory):
            file_path = os.path.join(directory, item)
            if os.path.isfile(file_path):
                if item.endswith('.json'):
                    process_json_file(file_path)
            elif os.path.isdir(file_path):
                process_directory(file_path)
    except Exception as e:
        print(f"Error processing directory {directory}: {str(e)}")

# Process the directory
process_directory(root_dir)

# Create the CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
    for user in post_likes:
        post_likes[user] = post_likes.get(user, 0)
        story_likes[user] = story_likes.get(user, 0)
        comments[user] = comments.get(user, 0)
        writer.writerow([user, post_likes[user], story_likes[user], comments[user]])

# Get the top 20 users
top_users = sorted(post_likes.items(), key=lambda x: x[1], reverse=True)[:20]

# Write the top 20 users to the CSV file
with open('query_responses/results.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for user, likes in top_users:
        writer.writerow([user, post_likes.get(user, 0), story_likes.get(user, 0), comments.get(user, 0)])
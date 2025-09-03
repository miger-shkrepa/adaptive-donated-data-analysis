import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the dictionaries to store the data
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
                # Process the item and update the dictionaries
                if 'likes_media_likes' in item:
                    for like in item['likes_media_likes']:
                        post_likes[item['title']] = post_likes.get(item['title'], 0) + len(like['string_list_data'])
                elif 'story_activities_story_likes' in item:
                    for like in item['story_activities_story_likes']:
                        story_likes[item['title']] = story_likes.get(item['title'], 0) + len(like['string_list_data'])
                elif 'comments_reels_comments' in item:
                    for comment in item['comments_reels_comments']:
                        comments[item['title']] = comments.get(item['title'], 0) + 1
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")

# Function to process the directory
def process_directory(directory):
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            if file.endswith('.json'):
                process_json_file(file_path)
        elif os.path.isdir(file_path):
            process_directory(file_path)

# Process the directory
process_directory(root_dir)

# Create a dictionary to store the top 20 accounts
top_accounts = {}
for account in post_likes:
    top_accounts[account] = {'Post Likes': post_likes[account], 'Story Likes': story_likes.get(account, 0), 'Comments': comments.get(account, 0)}

# Sort the accounts by the sum of their interactions
top_accounts = dict(sorted(top_accounts.items(), key=lambda item: sum(item[1].values()), reverse=True)[:20])

# Create a list to store the data for the CSV file
data = []
for account, interactions in top_accounts.items():
    data.append([account, interactions['Post Likes'], interactions['Story Likes'], interactions['Comments']])

# Write the data to the CSV file
with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
    writer.writerows(data)
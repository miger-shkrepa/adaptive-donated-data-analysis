import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize variables to store the data
account_views = {}
video_views = {}

# Function to process the JSON files
def process_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            # Assuming the JSON data is in the format of a dictionary
            json_data = eval(data)
            # Process the data
            for key, value in json_data.items():
                if key == "shopping":
                    for file_name, file_data in value.items():
                        if file_name == "recently_viewed_items.json":
                            for item in file_data["structure"]["checkout_saved_recently_viewed_products"]:
                                account = item["string_map_data"]["Merchant Name"]["value"]
                                views = 1
                                if account in account_views:
                                    account_views[account] += views
                                else:
                                    account_views[account] = views
                elif key == "likes":
                    for file_name, file_data in value.items():
                        if file_name == "liked_posts.json":
                            for item in file_data["structure"]["likes_media_likes"]:
                                account = item["title"]
                                views = 1
                                if account in account_views:
                                    account_views[account] += views
                                else:
                                    account_views[account] = views
                        elif file_name == "liked_comments.json":
                            for item in file_data["structure"]["likes_comment_likes"]:
                                account = item["title"]
                                views = 1
                                if account in account_views:
                                    account_views[account] += views
                                else:
                                    account_views[account] = views
                elif key == "story_interactions":
                    for file_name, file_data in value.items():
                        if file_name == "story_likes.json":
                            for item in file_data["structure"]["story_activities_story_likes"]:
                                account = item["title"]
                                views = 1
                                if account in account_views:
                                    account_views[account] += views
                                else:
                                    account_views[account] = views
                elif key == "messages":
                    for file_name, file_data in value.items():
                        if file_name == "inbox":
                            for file_name, file_data in file_data.items():
                                if file_name == "message_1.json":
                                    for item in file_data["structure"]["messages"]:
                                        account = item["sender_name"]
                                        views = 1
                                        if account in account_views:
                                            account_views[account] += views
                                        else:
                                            account_views[account] = views
    except Exception as e:
        print(f"Error processing file: {e}")

# Function to process the directory structure
def process_directory_structure():
    try:
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith(".json"):
                    process_json_file(file_path)
    except Exception as e:
        print(f"Error processing directory structure: {e}")

# Process the directory structure
process_directory_structure()

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account", "Post Views", "Video Views"])
    for account, views in account_views.items():
        writer.writerow([account, views, 0])

print("CSV file generated successfully.")
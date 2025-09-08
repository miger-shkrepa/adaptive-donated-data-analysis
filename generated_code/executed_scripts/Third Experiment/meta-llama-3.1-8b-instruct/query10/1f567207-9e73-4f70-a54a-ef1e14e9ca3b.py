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

# Define a function to process the JSON files
def process_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            # Assuming the JSON data is in the format of a dictionary
            json_data = eval(data)
            # Process the data and store it in the variables
            for item in json_data['ads_information']['ads_and_topics']['posts_viewed.json']['structure']['impressions_history_posts_seen']:
                account = item['string_map_data']['Author']['value']
                if account in account_views:
                    account_views[account] += 1
                else:
                    account_views[account] = 1
            for item in json_data['ads_information']['ads_and_topics']['videos_watched.json']['structure']['impressions_history_videos_watched']:
                account = item['string_map_data']['Author']['value']
                if account in video_views:
                    video_views[account] += 1
                else:
                    video_views[account] = 1
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")

# Define a function to process the directory
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

# Create a CSV file to store the results
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Account', 'Post Views', 'Video Views'])
    for account, views in account_views.items():
        writer.writerow([account, views, video_views.get(account, 0)])

print("Query completed successfully.")
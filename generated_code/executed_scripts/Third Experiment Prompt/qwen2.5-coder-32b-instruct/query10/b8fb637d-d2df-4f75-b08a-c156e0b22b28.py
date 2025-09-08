import os
import csv

# Define the root directory
root_dir = "root_dir"

# Function to read JSON files
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return eval(file.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except Exception as e:
        raise ValueError(f"ValueError: Error reading the file {file_path}: {str(e)}")

# Function to extract post and video views
def extract_views(data):
    post_views = {}
    video_views = {}

    if 'ads_information' in data and 'ads_and_topics' in data['ads_information']:
        ads_and_topics = data['ads_information']['ads_and_topics']
        
        # Extract post views
        if 'posts_viewed.json' in ads_and_topics:
            posts_viewed = read_json_file(os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json'))
            if 'impressions_history_posts_seen' in posts_viewed:
                for post in posts_viewed['impressions_history_posts_seen']:
                    author = post['string_map_data']['Author']['value']
                    if author in post_views:
                        post_views[author] += 1
                    else:
                        post_views[author] = 1
        
        # Extract video views
        if 'videos_watched.json' in ads_and_topics:
            videos_watched = read_json_file(os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'videos_watched.json'))
            if 'impressions_history_videos_watched' in videos_watched:
                for video in videos_watched['impressions_history_videos_watched']:
                    author = video['string_map_data']['Author']['value']
                    if author in video_views:
                        video_views[author] += 1
                    else:
                        video_views[author] = 1

    return post_views, video_views

# Main function to process the directory and generate the CSV
def generate_csv():
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Extract views
        post_views, video_views = extract_views({})

        # Prepare the data for CSV
        data = []
        for account in set(post_views.keys()).union(set(video_views.keys())):
            post_count = post_views.get(account, 0)
            video_count = video_views.get(account, 0)
            data.append([account, post_count, video_count])

        # Write to CSV
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Account', 'Post Views', 'Video Views'])
            csvwriter.writerows(data)

    except Exception as e:
        # If any error occurs, write only the headers to the CSV
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Account', 'Post Views', 'Video Views'])
        print(f"Error: {str(e)}")

# Execute the main function
generate_csv()
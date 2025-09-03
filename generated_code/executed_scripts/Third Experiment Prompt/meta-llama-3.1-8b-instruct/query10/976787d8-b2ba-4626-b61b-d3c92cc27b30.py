import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account", "Post Views", "Video Views"])

    # Iterate over the 'ads_information' directory
    for account in os.listdir(os.path.join(root_dir, "ads_information")):
        if account == "ads_and_topics":
            # Iterate over the 'posts_viewed.json' and 'videos_watched.json' files
            for file in ["posts_viewed.json", "videos_watched.json"]:
                file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", file)
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'r') as json_file:
                            data = json.load(json_file)
                            # Extract the impressions history posts seen and videos watched
                            if "impressions_history_posts_seen" in data and "impressions_history_videos_watched" in data:
                                post_views = data["impressions_history_posts_seen"]
                                video_views = data["impressions_history_videos_watched"]
                                # Calculate the total post and video views
                                total_post_views = sum(len(post["string_map_data"]) for post in post_views)
                                total_video_views = sum(len(video["string_map_data"]) for video in video_views)
                                # Write the data to the CSV file
                                writer.writerow(["ads_and_topics", total_post_views, total_video_views])
                            else:
                                # If the key does not exist, treat its contribution as 0
                                writer.writerow(["ads_and_topics", 0, 0])
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON file: {e}")
                        writer.writerow(["ads_and_topics", 0, 0])
                else:
                    # If the file does not exist, treat its contribution as 0
                    writer.writerow(["ads_and_topics", 0, 0])
        else:
            # If the account is not 'ads_and_topics', skip it
            continue
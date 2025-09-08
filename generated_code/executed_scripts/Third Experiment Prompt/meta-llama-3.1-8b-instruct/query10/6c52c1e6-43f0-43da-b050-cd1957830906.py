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

    # Iterate over the directory structure
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".json"):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r') as json_file:
                        data = json.load(json_file)
                        if "ads_information" in data and "ads_and_topics" in data["ads_information"]:
                            for file in data["ads_information"]["ads_and_topics"].values():
                                if file["type"] == "json":
                                    if "impressions_history_ads_seen" in file["structure"]:
                                        for item in file["structure"]["impressions_history_ads_seen"]:
                                            if "string_map_data" in item:
                                                for key, value in item["string_map_data"].items():
                                                    if key == "Author":
                                                        account = value["value"]
                                                        post_views = 1
                                                    elif key == "Time":
                                                        video_views = 1
                                                writer.writerow([account, post_views, video_views])
                                    elif "impressions_history_posts_seen" in file["structure"]:
                                        for item in file["structure"]["impressions_history_posts_seen"]:
                                            if "string_map_data" in item:
                                                for key, value in item["string_map_data"].items():
                                                    if key == "Author":
                                                        account = value["value"]
                                                        post_views = 1
                                                    elif key == "Time":
                                                        video_views = 1
                                                writer.writerow([account, post_views, video_views])
                                    elif "impressions_history_videos_watched" in file["structure"]:
                                        for item in file["structure"]["impressions_history_videos_watched"]:
                                            if "string_map_data" in item:
                                                for key, value in item["string_map_data"].items():
                                                    if key == "Author":
                                                        account = value["value"]
                                                        post_views = 1
                                                    elif key == "Time":
                                                        video_views = 1
                                                writer.writerow([account, post_views, video_views])
                        elif "your_instagram_activity" in data and "content" in data["your_instagram_activity"]:
                            for file in data["your_instagram_activity"]["content"].values():
                                if file["type"] == "json":
                                    if "ig_profile_picture" in file["structure"]:
                                        for item in file["structure"]["ig_profile_picture"]:
                                            if "title" in item:
                                                account = item["title"]
                                                post_views = 1
                                                video_views = 1
                                        writer.writerow([account, post_views, video_views])
                except json.JSONDecodeError:
                    print(f"Error: Failed to parse JSON file {filepath}")
                except KeyError:
                    print(f"Error: Missing key in JSON file {filepath}")
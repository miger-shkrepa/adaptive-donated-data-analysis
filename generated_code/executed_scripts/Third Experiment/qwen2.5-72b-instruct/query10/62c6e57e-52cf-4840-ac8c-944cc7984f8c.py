import os
import json
import csv

root_dir = "root_dir"

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    # Initialize a dictionary to store the aggregated data
    aggregated_data = {}

    # Check if the necessary directories exist
    if os.path.exists(os.path.join(root_dir, "activity")):
        activity_dir = os.path.join(root_dir, "activity")
        if os.path.exists(os.path.join(activity_dir, "post_views.json")):
            with open(os.path.join(activity_dir, "post_views.json"), 'r') as file:
                post_views_data = json.load(file)
                for entry in post_views_data.get("story_activities_post_views", []):
                    title = entry.get("title", "")
                    for data in entry.get("string_list_data", []):
                        timestamp = data.get("timestamp", 0)
                        if title in aggregated_data:
                            aggregated_data[title]["Post Views"] += 1
                        else:
                            aggregated_data[title] = {"Post Views": 1, "Video Views": 0}

        if os.path.exists(os.path.join(activity_dir, "video_views.json")):
            with open(os.path.join(activity_dir, "video_views.json"), 'r') as file:
                video_views_data = json.load(file)
                for entry in video_views_data.get("story_activities_video_views", []):
                    title = entry.get("title", "")
                    for data in entry.get("string_list_data", []):
                        timestamp = data.get("timestamp", 0)
                        if title in aggregated_data:
                            aggregated_data[title]["Video Views"] += 1
                        else:
                            aggregated_data[title] = {"Post Views": 0, "Video Views": 1}

    # Write the aggregated data to a CSV file
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, views in aggregated_data.items():
            writer.writerow({'Account': account, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})

except FileNotFoundError as e:
    print(e)
except json.JSONDecodeError as e:
    raise ValueError(f"Error: JSON decoding error - {str(e)}")
except Exception as e:
    raise Exception(f"Error: An unexpected error occurred - {str(e)}")
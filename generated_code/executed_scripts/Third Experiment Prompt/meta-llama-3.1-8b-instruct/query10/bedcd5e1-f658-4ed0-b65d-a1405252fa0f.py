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
                        post_views = 0
                        video_views = 0
                        account = os.path.basename(dirpath)

                        # Check if the file contains post views
                        if "ads_information" in data and "ads_and_topics" in data["ads_information"] and "ads_viewed.json" in data["ads_information"]["ads_and_topics"]:
                            for item in data["ads_information"]["ads_and_topics"]["ads_viewed.json"]["structure"]["impressions_history_ads_seen"]:
                                if "string_map_data" in item and "Author" in item["string_map_data"] and "value" in item["string_map_data"]["Author"]:
                                    post_views += 1
                                if "string_map_data" in item and "Time" in item["string_map_data"] and "timestamp" in item["string_map_data"]["Time"]:
                                    video_views += 1

                        # Check if the file contains video views
                        elif "ads_information" in data and "instagram_ads_and_businesses" in data["ads_information"] and "ads_about_meta.json" in data["instagram_ads_and_businesses"]:
                            for item in data["ads_information"]["instagram_ads_and_businesses"]["ads_about_meta.json"]["structure"]["label_values"]:
                                if "label" in item and item["label"] == "Post Views":
                                    post_views = item["timestamp_value"]
                                elif "label" in item and item["label"] == "Video Views":
                                    video_views = item["timestamp_value"]

                        # Write the result to the CSV file
                        writer.writerow([account, post_views, video_views])
                except json.JSONDecodeError:
                    print(f"Error: Failed to parse JSON file {filepath}")
                except KeyError as e:
                    print(f"Error: Missing key {e} in JSON file {filepath}")
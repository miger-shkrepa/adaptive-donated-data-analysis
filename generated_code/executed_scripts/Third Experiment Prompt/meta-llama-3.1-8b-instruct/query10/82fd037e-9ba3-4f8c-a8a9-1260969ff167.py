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

    # Iterate over the ads_information directory
    for account in os.listdir(os.path.join(root_dir, "ads_information", "ads_and_topics")):
        post_views = 0
        video_views = 0

        # Check if the account is a JSON file
        if account.endswith(".json"):
            try:
                with open(os.path.join(root_dir, "ads_information", "ads_and_topics", account), 'r') as json_file:
                    data = json.load(json_file)

                    # Check if the data has a 'structure' key
                    if 'structure' in data:
                        # Iterate over the impressions_history_ads_seen and impressions_history_posts_seen arrays
                        for item in data["structure"].get("impressions_history_ads_seen", []) + data["structure"].get("impressions_history_posts_seen", []):
                            # Check if the item has a string_map_data dictionary
                            if "string_map_data" in item:
                                # Iterate over the string_map_data dictionary
                                for key, value in item["string_map_data"].items():
                                    # Check if the key is "Author" or "Time"
                                    if key in ["Author", "Time"]:
                                        # Increment the post views or video views counter
                                        if key == "Author":
                                            post_views += 1
                                        elif key == "Time":
                                            video_views += 1

                # Write the account, post views, and video views to the CSV file
                writer.writerow([account, post_views, video_views])
            except FileNotFoundError:
                # If the file does not exist, treat its contribution as 0 and continue processing the rest
                writer.writerow([account, 0, 0])
            except json.JSONDecodeError:
                # If the file is not a valid JSON, treat its contribution as 0 and continue processing the rest
                writer.writerow([account, 0, 0])
import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list of accounts
accounts = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the file and load the JSON data
        with open(os.path.join(root_dir, filename), 'r') as f:
            data = json.load(f)

        # Check if the file contains the required data
        if "ads_information" in data and "ads_and_topics" in data["ads_information"] and "ads_viewed.json" in data["ads_information"]["ads_and_topics"]:
            # Load the ads_viewed.json file
            with open(os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json"), 'r') as f:
                ads_viewed_data = json.load(f)

            # Check if the file contains the required data
            if "impressions_history_ads_seen" in ads_viewed_data["structure"]:
                # Load the impressions_history_ads_seen data
                with open(os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json"), 'r') as f:
                    impressions_history_ads_seen_data = json.load(f)

                # Check if the file contains the required data
                if "string_map_data" in impressions_history_ads_seen_data["structure"]["impressions_history_ads_seen"][0]:
                    # Load the string_map_data data
                    with open(os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json"), 'r') as f:
                        string_map_data = json.load(f)

                    # Check if the file contains the required data
                    if "Author" in string_map_data["structure"]["impressions_history_ads_seen"][0]["string_map_data"]:
                        # Load the Author data
                        with open(os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json"), 'r') as f:
                            author_data = json.load(f)

                        # Check if the file contains the required data
                        if "likes" in author_data["structure"]["impressions_history_ads_seen"][0]["string_map_data"]:
                            # Load the likes data
                            with open(os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json"), 'r') as f:
                                likes_data = json.load(f)

                            # Check if the file contains the required data
                            if "likes_media_likes" in likes_data["structure"]:
                                # Load the likes_media_likes data
                                with open(os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json"), 'r') as f:
                                    likes_media_likes_data = json.load(f)

                                # Check if the file contains the required data
                                if "string_list_data" in likes_media_likes_data["structure"]["likes_media_likes"][0]:
                                    # Load the string_list_data data
                                    with open(os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json"), 'r') as f:
                                        string_list_data = json.load(f)

                                    # Check if the file contains the required data
                                    if "value" in string_list_data["structure"]["likes_media_likes"][0]["string_list_data"][0]:
                                        # Add the account to the list of accounts
                                        accounts.append(filename.split(".")[0])

# Write the list of accounts to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account"])
    writer.writerows([[account] for account in accounts])
import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the accounts
accounts = []

# Iterate over the 'ads_information' directory
for file in os.listdir(os.path.join(root_dir, "ads_information")):
    if file.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, "ads_information", file), "r") as f:
            data = json.load(f)
            # Check if the file contains the required structure
            if "ads_and_topics" in data and "ads_viewed.json" in data["ads_and_topics"]:
                # Open the 'ads_viewed.json' file
                with open(os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json"), "r") as f:
                    ads_viewed_data = json.load(f)
                    # Check if the file contains the required structure
                    if "impressions_history_ads_seen" in ads_viewed_data["structure"]:
                        # Open the 'posts_viewed.json' file
                        with open(os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json"), "r") as f:
                            posts_viewed_data = json.load(f)
                            # Check if the file contains the required structure
                            if "impressions_history_posts_seen" in posts_viewed_data["structure"]:
                                # Iterate over the 'impressions_history_posts_seen' list
                                for post in posts_viewed_data["structure"]["impressions_history_posts_seen"]:
                                    # Check if the post has a 'string_map_data' key
                                    if "string_map_data" in post:
                                        # Iterate over the 'string_map_data' dictionary
                                        for key, value in post["string_map_data"].items():
                                            # Check if the key is 'Author'
                                            if key == "Author":
                                                # Get the author's name
                                                author = value["value"]
                                                # Check if the author is in the 'ads_viewed.json' file
                                                if author in [msg["sender_name"] for msg in ads_viewed_data["structure"]["impressions_history_ads_seen"]]:
                                                    # Add the author to the accounts list
                                                    accounts.append(author)

# Write the accounts to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Account"])
    writer.writerows([[account] for account in accounts])
import os
import json
import csv

root_dir = "root_dir"

def get_account_views(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a dictionary to store the account views
        account_views = {}

        # Iterate over the subdirectories in the root directory
        for subdir in os.listdir(root_dir):
            subdir_path = os.path.join(root_dir, subdir)

            # Check if the subdirectory is a directory
            if os.path.isdir(subdir_path):
                # Iterate over the files in the subdirectory
                for filename in os.listdir(subdir_path):
                    file_path = os.path.join(subdir_path, filename)

                    # Check if the file is a JSON file
                    if filename.endswith(".json"):
                        # Open the JSON file
                        with open(file_path, "r") as file:
                            data = json.load(file)

                            # Check if the file contains post views or video views
                            if "impressions_history_posts_seen" in data:
                                # Iterate over the post views
                                for post_view in data["impressions_history_posts_seen"]:
                                    # Get the account name
                                    account = post_view["string_map_data"]["Author"]["value"]

                                    # Increment the post views for the account
                                    if account in account_views:
                                        account_views[account]["Post Views"] += 1
                                    else:
                                        account_views[account] = {"Post Views": 1, "Video Views": 0}

                            elif "impressions_history_videos_watched" in data:
                                # Iterate over the video views
                                for video_view in data["impressions_history_videos_watched"]:
                                    # Get the account name
                                    account = video_view["string_map_data"]["Author"]["value"]

                                    # Increment the video views for the account
                                    if account in account_views:
                                        account_views[account]["Video Views"] += 1
                                    else:
                                        account_views[account] = {"Post Views": 0, "Video Views": 1}

        # Return the account views
        return account_views

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(account_views):
    try:
        # Open the CSV file
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)

            # Write the header
            writer.writerow(["Account", "Post Views", "Video Views"])

            # Write the account views
            for account, views in account_views.items():
                writer.writerow([account, views["Post Views"], views["Video Views"]])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        # Get the account views
        account_views = get_account_views(root_dir)

        # Save the account views to a CSV file
        save_to_csv(account_views)

    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()
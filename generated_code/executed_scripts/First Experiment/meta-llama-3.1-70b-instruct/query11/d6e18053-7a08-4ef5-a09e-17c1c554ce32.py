import os
import json
import csv

root_dir = "root_dir"

def get_viewed_posts_but_not_liked(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        viewed_posts = set()
        liked_posts = set()

        # Iterate over all files in the directory
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                # Check if the file is a JSON file
                if filename.endswith(".json"):
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, "r") as file:
                        data = json.load(file)

                        # Check if the file contains viewed posts
                        if filename == "event_reminders.json" or filename == "messages.json":
                            for item in data.get("events_event_reminders", []) or data.get("messages", []):
                                for string_data in item.get("string_list_data", []):
                                    viewed_posts.add(string_data.get("value"))

                        # Check if the file contains liked posts
                        if filename == "liked_posts.json":
                            for item in data.get("likes_media_likes", []):
                                for string_data in item.get("string_list_data", []):
                                    liked_posts.add(string_data.get("value"))

        # Find posts that have been viewed but not liked
        viewed_but_not_liked = viewed_posts - liked_posts

        # Create a CSV file with the results
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account"])
            for post in viewed_but_not_liked:
                writer.writerow([post])

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: Error parsing JSON - {e}")
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred - {e}")

get_viewed_posts_but_not_liked(root_dir)
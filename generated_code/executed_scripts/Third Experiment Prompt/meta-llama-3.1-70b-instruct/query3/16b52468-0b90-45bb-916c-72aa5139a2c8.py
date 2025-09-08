import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_posts_viewed(root_dir):
    posts_viewed = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == "posts_viewed.json":
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        for post in data["impressions_history_posts_seen"]:
                            timestamp = post["string_map_data"]["Time"]["timestamp"]
                            date = datetime.fromtimestamp(timestamp)
                            date_str = date.strftime("%Y-%m-%d")
                            week_str = date.strftime("Week %Y-%W")
                            if date_str not in posts_viewed:
                                posts_viewed[date_str] = 0
                            if week_str not in posts_viewed:
                                posts_viewed[week_str] = 0
                            posts_viewed[date_str] += 1
                            posts_viewed[week_str] += 1
                except FileNotFoundError:
                    raise FileNotFoundError("Error: The file 'posts_viewed.json' does not exist.")
                except json.JSONDecodeError:
                    raise ValueError("Error: The file 'posts_viewed.json' is not a valid JSON file.")
    return posts_viewed

def write_to_csv(posts_viewed):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        for date, count in posts_viewed.items():
            if date.startswith("Week"):
                writer.writerow([date, count, "Weekly"])
            else:
                writer.writerow([date, count, "Daily"])

def main():
    try:
        posts_viewed = get_posts_viewed(root_dir)
        write_to_csv(posts_viewed)
    except FileNotFoundError as e:
        print(e)
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])
    except ValueError as e:
        print(e)
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])

if __name__ == "__main__":
    main()
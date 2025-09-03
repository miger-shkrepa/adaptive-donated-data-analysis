import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_post_views(root_dir):
    post_views = {}
    for dir_name in os.listdir(root_dir):
        dir_path = os.path.join(root_dir, dir_name)
        if os.path.isdir(dir_path):
            for file_name in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file_name)
                if file_name.endswith(".json"):
                    try:
                        with open(file_path, "r") as file:
                            data = eval(file.read())
                            for message in data.get("messages", []):
                                timestamp_ms = message.get("timestamp_ms")
                                if timestamp_ms:
                                    date = datetime.fromtimestamp(timestamp_ms / 1000)
                                    date_str = date.strftime("%Y-%m-%d")
                                    week_str = f"Week {date.strftime('%Y-%U')}"
                                    post_views[date_str] = post_views.get(date_str, 0) + 1
                                    post_views[week_str] = post_views.get(week_str, 0) + 1
                    except Exception as e:
                        raise ValueError(f"Error: Failed to parse {file_path}: {str(e)}")
    return post_views

def write_csv(post_views):
    with open("query_responses/results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        for date_str, views in post_views.items():
            if date_str.startswith("Week"):
                writer.writerow([date_str, views, "Weekly"])
            else:
                writer.writerow([date_str, views, "Daily"])

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    post_views = get_post_views(root_dir)
    write_csv(post_views)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {str(e)}")
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])
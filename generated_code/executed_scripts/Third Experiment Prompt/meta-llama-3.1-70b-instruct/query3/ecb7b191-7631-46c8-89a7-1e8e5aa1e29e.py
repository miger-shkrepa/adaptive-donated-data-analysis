import os
import csv
import datetime
import json

root_dir = "root_dir"

def get_posts_viewed(root_dir):
    posts_viewed = {}
    try:
        ads_info_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
        posts_viewed_file = os.path.join(ads_info_dir, "posts_viewed.json")
        if os.path.exists(posts_viewed_file):
            with open(posts_viewed_file, "r") as f:
                data = json.load(f)
                for post in data["impressions_history_posts_seen"]:
                    timestamp = post["string_map_data"]["Time"]["timestamp"]
                    date = datetime.datetime.fromtimestamp(timestamp)
                    date_str = date.strftime("%Y-%m-%d")
                    week_str = date.strftime("Week %Y-%W")
                    if date_str not in posts_viewed:
                        posts_viewed[date_str] = 0
                    if week_str not in posts_viewed:
                        posts_viewed[week_str] = 0
                    posts_viewed[date_str] += 1
                    posts_viewed[week_str] += 1
        else:
            raise FileNotFoundError("Error: posts_viewed.json file not found")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")
    return posts_viewed

def write_to_csv(posts_viewed):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        fieldnames = ["Date/Week", "Posts Viewed", "Type"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for date, count in posts_viewed.items():
            if date.startswith("Week"):
                writer.writerow({"Date/Week": date, "Posts Viewed": count, "Type": "Weekly"})
            else:
                writer.writerow({"Date/Week": date, "Posts Viewed": count, "Type": "Daily"})

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")
        posts_viewed = get_posts_viewed(root_dir)
        write_to_csv(posts_viewed)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

if __name__ == "__main__":
    main()
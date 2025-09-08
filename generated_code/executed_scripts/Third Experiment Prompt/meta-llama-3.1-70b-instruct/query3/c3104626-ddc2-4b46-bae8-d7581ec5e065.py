import os
import csv
import datetime

root_dir = "root_dir"

def get_posts_viewed(root_dir):
    posts_viewed = {}
    for year in os.listdir(os.path.join(root_dir, "media", "posts")):
        year_dir = os.path.join(root_dir, "media", "posts", year)
        for file in os.listdir(year_dir):
            if file.endswith(".json"):
                with open(os.path.join(year_dir, file), "r") as f:
                    data = json.load(f)
                    for post in data:
                        timestamp = post["creation_timestamp"]
                        date = datetime.datetime.fromtimestamp(timestamp)
                        date_str = date.strftime("%Y-%m-%d")
                        week_str = date.strftime("Week %Y-%W")
                        if date_str not in posts_viewed:
                            posts_viewed[date_str] = 0
                        if week_str not in posts_viewed:
                            posts_viewed[week_str] = 0
                        posts_viewed[date_str] += 1
                        posts_viewed[week_str] += 1
    return posts_viewed

def write_csv(posts_viewed):
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
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")
        posts_viewed = get_posts_viewed(root_dir)
        write_csv(posts_viewed)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

if __name__ == "__main__":
    main()
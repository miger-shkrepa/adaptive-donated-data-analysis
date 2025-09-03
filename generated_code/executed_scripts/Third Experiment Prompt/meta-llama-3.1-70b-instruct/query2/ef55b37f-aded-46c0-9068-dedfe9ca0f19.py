import os
import json
import csv

root_dir = "root_dir"

def get_ads_viewed(root_dir):
    try:
        ads_and_topics_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
        if not os.path.exists(ads_and_topics_dir):
            raise FileNotFoundError("FileNotFoundError: The ads_and_topics directory does not exist.")

        posts_viewed_file = os.path.join(ads_and_topics_dir, "posts_viewed.json")
        if not os.path.exists(posts_viewed_file):
            raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")

        with open(posts_viewed_file, "r") as file:
            posts_viewed_data = json.load(file)

        ads_viewed = {}
        for post in posts_viewed_data.get("impressions_history_posts_seen", []):
            author = post.get("string_map_data", {}).get("Author", {}).get("value")
            if author not in ads_viewed:
                ads_viewed[author] = 1
            else:
                ads_viewed[author] += 1

        videos_watched_file = os.path.join(ads_and_topics_dir, "videos_watched.json")
        if os.path.exists(videos_watched_file):
            with open(videos_watched_file, "r") as file:
                videos_watched_data = json.load(file)

            for video in videos_watched_data.get("impressions_history_videos_watched", []):
                author = video.get("string_map_data", {}).get("Author", {}).get("value")
                if author not in ads_viewed:
                    ads_viewed[author] = 1
                else:
                    ads_viewed[author] += 1

        return ads_viewed

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")

def write_to_csv(ads_viewed):
    try:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            for company, count in ads_viewed.items():
                writer.writerow([company, count])

    except Exception as e:
        raise Exception(f"Error: Failed to write to CSV file: {e}")

def main():
    try:
        ads_viewed = get_ads_viewed(root_dir)
        if ads_viewed:
            write_to_csv(ads_viewed)
        else:
            with open("query_responses/results.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Company Name", "Number of Ads Viewed"])

    except FileNotFoundError as e:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
        print(f"FileNotFoundError: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
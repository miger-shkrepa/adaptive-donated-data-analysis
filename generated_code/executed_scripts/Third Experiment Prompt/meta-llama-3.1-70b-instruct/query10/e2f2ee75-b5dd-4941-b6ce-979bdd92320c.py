import os
import json
import csv

root_dir = "root_dir"

def get_views(root_dir):
    views = {}
    try:
        # Get post views
        post_views_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        if os.path.exists(post_views_file):
            with open(post_views_file, "r") as f:
                post_views_data = json.load(f)
                for post_view in post_views_data["impressions_history_posts_seen"]:
                    string_map_data = post_view.get("string_map_data", {})
                    account = string_map_data.get("Author", {}).get("value")
                    if account:
                        if account not in views:
                            views[account] = {"Post Views": 0, "Video Views": 0}
                        views[account]["Post Views"] += 1
        else:
            print("Warning: posts_viewed.json not found. Assuming 0 post views.")

        # Get video views
        video_views_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")
        if os.path.exists(video_views_file):
            with open(video_views_file, "r") as f:
                video_views_data = json.load(f)
                for video_view in video_views_data["impressions_history_videos_watched"]:
                    string_map_data = video_view.get("string_map_data", {})
                    account = string_map_data.get("Author", {}).get("value")
                    if account:
                        if account not in views:
                            views[account] = {"Post Views": 0, "Video Views": 0}
                        views[account]["Video Views"] += 1
        else:
            print("Warning: videos_watched.json not found. Assuming 0 video views.")

    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory does not exist.")
    except json.JSONDecodeError as e:
        raise ValueError("Error: Invalid JSON format in file. " + str(e))
    except Exception as e:
        raise Exception("Error: An unexpected error occurred. " + str(e))

    return views

def write_csv(views):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        fieldnames = ["Account", "Post Views", "Video Views"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, view_counts in views.items():
            writer.writerow({"Account": account, "Post Views": view_counts["Post Views"], "Video Views": view_counts["Video Views"]})

def main():
    views = get_views(root_dir)
    if not views:
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            fieldnames = ["Account", "Post Views", "Video Views"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    else:
        write_csv(views)

if __name__ == "__main__":
    main()
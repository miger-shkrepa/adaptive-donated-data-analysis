import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Function to extract post and video views
def extract_views(root_dir):
    post_views = {}
    video_views = {}

    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    # Define the paths for the JSON files
    posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    videos_watched_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")

    # Process posts_viewed.json
    if os.path.exists(posts_viewed_path):
        with open(posts_viewed_path, 'r') as file:
            data = json.load(file)
            for entry in data.get("impressions_history_posts_seen", []):
                author = entry.get("string_map_data", {}).get("Author", {}).get("value", "")
                time = entry.get("string_map_data", {}).get("Time", {}).get("timestamp", 0)
                if author:
                    if author not in post_views:
                        post_views[author] = 0
                    post_views[author] += 1
    else:
        raise FileNotFoundError("Error: posts_viewed.json does not exist.")

    # Process videos_watched.json
    if os.path.exists(videos_watched_path):
        with open(videos_watched_path, 'r') as file:
            data = json.load(file)
            for entry in data.get("impressions_history_videos_watched", []):
                author = entry.get("string_map_data", {}).get("Author", {}).get("value", "")
                time = entry.get("string_map_data", {}).get("Time", {}).get("timestamp", 0)
                if author:
                    if author not in video_views:
                        video_views[author] = 0
                    video_views[author] += 1
    else:
        raise FileNotFoundError("Error: videos_watched.json does not exist.")

    return post_views, video_views

# Function to write the results to a CSV file
def write_to_csv(post_views, video_views):
    # Create the output directory if it does not exist
    output_dir = "query_responses"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define the path for the output CSV file
    output_path = os.path.join(output_dir, "results.csv")

    # Write the data to the CSV file
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ["Account", "Post Views", "Video Views"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for account in set(post_views.keys()).union(video_views.keys()):
            writer.writerow({
                "Account": account,
                "Post Views": post_views.get(account, 0),
                "Video Views": video_views.get(account, 0)
            })

# Main function to execute the script
def main():
    try:
        post_views, video_views = extract_views(root_dir)
        write_to_csv(post_views, video_views)
        print("CSV file generated successfully at 'query_responses/results.csv'")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
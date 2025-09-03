import os
import csv
from datetime import datetime, timedelta

root_dir = "root_dir"

def get_files_in_directory(directory, extension):
    try:
        return [f for f in os.listdir(directory) if f.endswith(extension)]
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred while accessing the directory: {str(e)}")

def parse_timestamp(timestamp):
    try:
        return datetime.fromtimestamp(int(timestamp))
    except ValueError:
        raise ValueError("ValueError: Invalid timestamp format.")

def aggregate_post_views(root_dir):
    story_interactions_dir = os.path.join(root_dir, "story_interactions")
    if not os.path.exists(story_interactions_dir):
        return []

    post_views = []
    for json_file in get_files_in_directory(story_interactions_dir, ".json"):
        file_path = os.path.join(story_interactions_dir, json_file)
        try:
            with open(file_path, 'r') as file:
                data = eval(file.read())
                for activity in data.get(f"story_activities_{json_file.split('.')[0]}", []):
                    for entry in activity.get("string_list_data", []):
                        timestamp = entry.get("timestamp")
                        if timestamp:
                            post_views.append(parse_timestamp(timestamp))
        except FileNotFoundError:
            raise FileNotFoundError(f"FileNotFoundError: The file {json_file} does not exist.")
        except Exception as e:
            raise ValueError(f"ValueError: An error occurred while reading the file {json_file}: {str(e)}")

    return post_views

def generate_csv(post_views):
    daily_counts = {}
    weekly_counts = {}

    for timestamp in post_views:
        date_str = timestamp.strftime('%Y-%m-%d')
        week_str = f"Week {timestamp.strftime('%Y-%W')}"

        if date_str in daily_counts:
            daily_counts[date_str] += 1
        else:
            daily_counts[date_str] = 1

        if week_str in weekly_counts:
            weekly_counts[week_str] += 1
        else:
            weekly_counts[week_str] = 1

    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])

        for date, count in sorted(daily_counts.items()):
            writer.writerow([date, count, 'Daily'])

        for week, count in sorted(weekly_counts.items()):
            writer.writerow([week, count, 'Weekly'])

def main():
    try:
        post_views = aggregate_post_views(root_dir)
        generate_csv(post_views)
    except Exception as e:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])

if __name__ == "__main__":
    main()
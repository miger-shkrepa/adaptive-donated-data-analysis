import json
import os
from collections import Counter
from datetime import datetime
import csv

def find_file(base_folder, target_file):
    for root, _, files in os.walk(base_folder):
        if target_file in files:
            return os.path.join(root, target_file)
    return None

def analyze_post_views(base_folder):
    target_file = "posts_viewed.json"
    file_path = find_file(base_folder, target_file)

    if not file_path:
        print(f"Warning: {target_file} not found in {base_folder}. Skipping.")
        return None, None

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    daily_counter = Counter()
    weekly_counter = Counter()

    for entry in data.get("impressions_history_posts_seen", []):
        timestamp = entry.get("string_map_data", {}).get("Time", {}).get("timestamp")
        if timestamp:
            dt = datetime.fromtimestamp(timestamp)
            date_str = dt.strftime("%Y-%m-%d")
            week_str = f"Week {dt.strftime('%Y-%W')}"
            daily_counter[date_str] += 1
            weekly_counter[week_str] += 1

    return daily_counter, weekly_counter

def save_combined_csv(daily_counter, weekly_counter, output_file):
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])
            for date, count in sorted(daily_counter.items()):
                writer.writerow([date, count, "Daily"])
            for week, count in sorted(weekly_counter.items()):
                writer.writerow([week, count, "Weekly"])
        print(f"✅ Saved: {output_file}")
    except Exception as e:
        print(f"❌ Error writing CSV: {e}")

def main():
    datasets_dir = "../../datasets"
    output_dir = os.path.join("../../ground_truths", "query3_1")
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.isdir(datasets_dir):
        print(f"Error: Directory '{datasets_dir}' does not exist.")
        return

    for subdir in os.listdir(datasets_dir):
        full_path = os.path.join(datasets_dir, subdir)
        if not os.path.isdir(full_path):
            continue

        daily_counts, weekly_counts = analyze_post_views(full_path)

        if daily_counts is None and weekly_counts is None:
            output_file = os.path.join(output_dir, f"NODATA_{subdir}_ground_truth.csv")
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Date/Week", "Posts Viewed", "Type"])
            print(f"⚠️  No data file found. Created placeholder: {output_file}")
            continue

        if not daily_counts and not weekly_counts:
            continue

        output_file = os.path.join(output_dir, f"{subdir}_ground_truth.csv")
        save_combined_csv(daily_counts, weekly_counts, output_file)

if __name__ == "__main__":
    main()

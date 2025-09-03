import json
import os
import csv
from collections import defaultdict

def find_content_files(dataset_path):
    posts_file = None
    videos_file = None

    for root, _, files in os.walk(dataset_path):
        if 'posts_viewed.json' in files:
            posts_file = os.path.join(root, 'posts_viewed.json')
        if 'videos_watched.json' in files:
            videos_file = os.path.join(root, 'videos_watched.json')
        if posts_file or videos_file:
            break

    return posts_file, videos_file

def analyze_content_views(posts_file, videos_file):
    stats = defaultdict(lambda: {'posts': 0, 'videos': 0})

    if posts_file:
        try:
            with open(posts_file, 'r', encoding='utf-8') as f:
                posts_data = json.load(f)
                for post in posts_data.get('impressions_history_posts_seen', []):
                    author = post.get('string_map_data', {}).get('Author', {}).get('value', 'Unknown')
                    stats[author]['posts'] += 1
        except Exception as e:
            print(f"⚠️  Failed to process posts: {e}")

    if videos_file:
        try:
            with open(videos_file, 'r', encoding='utf-8') as f:
                videos_data = json.load(f)
                for video in videos_data.get('impressions_history_videos_watched', []):
                    author = video.get('string_map_data', {}).get('Author', {}).get('value', 'Unknown')
                    stats[author]['videos'] += 1
        except Exception as e:
            print(f"⚠️  Failed to process videos: {e}")

    return stats

def export_csv(stats, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Account', 'Post Views', 'Video Views'])

        sorted_accounts = sorted(stats.items(), key=lambda x: x[1]['posts'] + x[1]['videos'], reverse=True)

        for account, data in sorted_accounts:
            writer.writerow([account, data['posts'], data['videos']])

def export_nodata(output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Account', 'Post Views', 'Video Views'])

    print(f"⚠️  No data files found. Created placeholder: {output_path}")

def main():
    datasets_dir = "../../datasets"
    output_dir = os.path.join("../../ground_truths", "query10")
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.isdir(datasets_dir):
        print(f"Error: Directory '{datasets_dir}' does not exist.")
        return

    for subdir in os.listdir(datasets_dir):
        sub_path = os.path.join(datasets_dir, subdir)
        if not os.path.isdir(sub_path):
            continue

        posts_file, videos_file = find_content_files(sub_path)

        if not posts_file and not videos_file:
            nodata_file = os.path.join(output_dir, f"NODATA_{subdir}_ground_truth.csv")
            export_nodata(nodata_file)
            continue

        stats = analyze_content_views(posts_file, videos_file)

        if not stats:
            nodata_file = os.path.join(output_dir, f"NODATA_{subdir}_ground_truth.csv")
            export_nodata(nodata_file)
            continue

        output_path = os.path.join(output_dir, f"{subdir}_ground_truth.csv")
        export_csv(stats, output_path)
        print(f"✅ Saved: {output_path}")

if __name__ == '__main__':
    main()

import json
import os
import csv
from collections import Counter

datasets_dir = "../../datasets"
output_dir = os.path.join("../../ground_truths", "query2")
os.makedirs(output_dir, exist_ok=True)

def find_file(base_folder, target_file):
    for root, _, files in os.walk(base_folder):
        if target_file in files:
            return os.path.join(root, target_file)
    return None

def analyze_ads(base_folder):
    try:
        file_path = find_file(base_folder, "ads_viewed.json")
        if not file_path:
            return None

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        ad_counts = Counter()
        for ad_data in data.get("impressions_history_ads_seen", []):
            string_map_data = ad_data.get("string_map_data", {})
            company = string_map_data.get("Author", {}).get("value")
            if company:
                ad_counts[company] += 1

        return ad_counts
    except Exception as e:
        print(f"Error analyzing ads: {e}")
        return None

def save_ad_analysis_to_csv(ad_counts, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name", "Number of Ads Viewed"])
        for company, count in ad_counts.items():
            writer.writerow([company, count])

def save_nodata_csv(output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Company Name", "Number of Ads Viewed"])

# === MAIN LOOP ===
for subdir in os.listdir(datasets_dir):
    full_path = os.path.join(datasets_dir, subdir)
    if not os.path.isdir(full_path):
        continue

    ad_counts = analyze_ads(full_path)

    if ad_counts:
        output_file = os.path.join(output_dir, f"{subdir}_ground_truth.csv")
        save_ad_analysis_to_csv(ad_counts, output_file)
        print(f"✅ Saved: {output_file}")
    else:
        nodata_file = os.path.join(output_dir, f"NODATA_{subdir}_ground_truth.csv")
        save_nodata_csv(nodata_file)
        print(f"⚠️  No ad data found. Created: {nodata_file}")

print("\n🎉 All datasets processed for query13.")

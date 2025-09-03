import json
import os
import csv

def find_file(base_folder, target_file):
    for root, _, files in os.walk(base_folder):
        if target_file in files:
            return os.path.join(root, target_file)
    return None

def extract_following(file_path):
    if not file_path:
        return set()
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    following = set()
    for entry in data.get("relationships_following", []):
        for item in entry.get("string_list_data", []):
            profile = item.get("value")
            if profile:
                following.add(profile)
    return following

def extract_followers(file_path):
    if not file_path:
        return set()
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    followers = set()
    for entry in data:
        for item in entry.get("string_list_data", []):
            profile = item.get("value")
            if profile:
                followers.add(profile)
    return followers

def get_not_following_back(following, followers):
    return sorted(following - followers)

def save_to_csv(profiles, output_file):
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Profile"])
            for profile in profiles:
                writer.writerow([profile])
        print(f"✅ Saved: {output_file}")
    except Exception as e:
        print(f"❌ Error writing CSV: {e}")

def main():
    datasets_dir = "../../datasets"
    output_dir = os.path.join("../../ground_truths", "query9")
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.isdir(datasets_dir):
        print(f"Error: Directory '{datasets_dir}' does not exist.")
        return

    for subdir in os.listdir(datasets_dir):
        full_path = os.path.join(datasets_dir, subdir)
        if not os.path.isdir(full_path):
            continue

        following_file = find_file(full_path, "following.json")
        followers_file = find_file(full_path, "followers_1.json")

        following = extract_following(following_file)
        followers = extract_followers(followers_file)

        not_following_back = get_not_following_back(following, followers)

        if not_following_back:
            output_file = os.path.join(output_dir, f"{subdir}_ground_truth.csv")
        else:
            output_file = os.path.join(output_dir, f"NODATA_{subdir}_ground_truth.csv")

        save_to_csv(not_following_back, output_file)

if __name__ == "__main__":
    main()

import json
import os
import csv

def find_required_files(main_directory):
    files = {'viewed': None, 'liked': None}
    for root, dirs, filenames in os.walk(main_directory):
        if 'posts_viewed.json' in filenames:
            files['viewed'] = os.path.join(root, 'posts_viewed.json')
        if 'liked_posts.json' in filenames:
            files['liked'] = os.path.join(root, 'liked_posts.json')
        if all(files.values()):
            break
    return files

def extract_accounts(file_path, interaction_type):
    accounts = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            key = 'impressions_history_posts_seen' if interaction_type == 'viewed' else 'likes_media_likes'
            for item in data.get(key, []):
                if interaction_type == 'viewed':
                    account = item.get('string_map_data', {}).get('Author', {}).get('value')
                else:
                    account = item.get('title')
                if account:
                    accounts.add(account)
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Warning: Could not process {interaction_type} file - {str(e)}")
    return accounts

def save_to_csv(accounts, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Account'])
        for account in sorted(accounts):
            writer.writerow([account])

def main():
    datasets_dir = "../../datasets"
    output_dir = "../../ground_truths/query11"
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.isdir(datasets_dir):
        print(f"Error: Directory '{datasets_dir}' does not exist.")
        return

    for subdir in os.listdir(datasets_dir):
        full_path = os.path.join(datasets_dir, subdir)
        if not os.path.isdir(full_path):
            continue

        files = find_required_files(full_path)
        viewed_accounts = extract_accounts(files['viewed'], 'viewed') if files['viewed'] else set()
        liked_accounts = extract_accounts(files['liked'], 'liked') if files['liked'] else set()

        if viewed_accounts:
            viewed_only_accounts = viewed_accounts - liked_accounts
            output_path = os.path.join(output_dir, f"{subdir}_ground_truth.csv")
            save_to_csv(viewed_only_accounts, output_path)
            print(f"✅ {subdir}: {len(viewed_only_accounts)} viewed-only accounts saved")
        else:
            output_path = os.path.join(output_dir, f"NODATA_{subdir}_ground_truth.csv")
            save_to_csv(set(), output_path)
            print(f"⚠️ {subdir}: No viewed accounts found — NODATA file created")

if __name__ == '__main__':
    main()

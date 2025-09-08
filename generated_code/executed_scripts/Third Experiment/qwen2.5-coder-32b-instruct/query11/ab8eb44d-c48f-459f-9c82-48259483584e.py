import os
import json
import csv

root_dir = "root_dir"

def get_accounts_from_json(file_path, key):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            accounts = set()
            for item in data.get(key, []):
                for entry in item.get('string_list_data', []):
                    accounts.add(entry.get('value'))
            return accounts
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while processing the file {file_path}: {str(e)}")

def main():
    saved_posts_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")
    liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")

    try:
        saved_accounts = get_accounts_from_json(saved_posts_path, 'saved_saved_media')
        liked_accounts = get_accounts_from_json(liked_posts_path, 'likes_media_likes')

        viewed_but_not_liked_accounts = saved_accounts - liked_accounts

        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for account in viewed_but_not_liked_accounts:
                writer.writerow([account])

    except Exception as e:
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])

        print(str(e))

if __name__ == "__main__":
    main()
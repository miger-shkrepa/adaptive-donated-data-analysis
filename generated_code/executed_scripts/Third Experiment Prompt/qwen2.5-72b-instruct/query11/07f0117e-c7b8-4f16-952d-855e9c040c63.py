import os
import json
import csv

root_dir = "root_dir"

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The JSON file is not properly formatted.")

def get_accounts_from_json(data, key_path):
    accounts = set()
    try:
        current_data = data
        for key in key_path:
            current_data = current_data[key]
        for item in current_data:
            for string_data in item['string_list_data']:
                accounts.add(string_data['value'])
    except KeyError:
        pass  # If the key is not found, just continue
    return accounts

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")

        liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        saved_posts_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")

        liked_accounts = set()
        saved_accounts = set()

        if os.path.exists(liked_posts_path):
            liked_posts_data = load_json_data(liked_posts_path)
            liked_accounts = get_accounts_from_json(liked_posts_data, ['likes_media_likes'])

        if os.path.exists(saved_posts_path):
            saved_posts_data = load_json_data(saved_posts_path)
            saved_accounts = get_accounts_from_json(saved_posts_data, ['saved_saved_media'])

        accounts_viewed_but_not_liked = saved_accounts - liked_accounts

        output_file = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for account in accounts_viewed_but_not_liked:
                writer.writerow([account])

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
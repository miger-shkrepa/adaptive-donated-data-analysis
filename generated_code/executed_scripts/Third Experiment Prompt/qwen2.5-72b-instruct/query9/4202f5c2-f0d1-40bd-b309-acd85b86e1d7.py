import os
import json
import csv

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def get_following_and_followers(root_dir):
    following = set()
    followers = set()

    following_file = os.path.join(root_dir, 'connections', 'followers_and_following', 'following.json')
    followers_file = os.path.join(root_dir, 'connections', 'followers_and_following', 'followers_1.json')

    if os.path.exists(following_file):
        data = load_json_file(following_file)
        for entry in data.get('following', {}).get('relationships_following', []):
            for string_data in entry.get('string_list_data', []):
                following.add(string_data.get('value'))

    if os.path.exists(followers_file):
        data = load_json_file(followers_file)
        for entry in data.get('followers_1', {}).get('relationships_followers', []):
            for string_data in entry.get('string_list_data', []):
                followers.add(string_data.get('value'))

    return following, followers

def find_non_mutual_follows(following, followers):
    return following - followers

def write_to_csv(profiles, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Profile'])
        for profile in profiles:
            writer.writerow([profile])

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        following, followers = get_following_and_followers(root_dir)
        non_mutual_follows = find_non_mutual_follows(following, followers)

        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        write_to_csv(non_mutual_follows, output_path)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
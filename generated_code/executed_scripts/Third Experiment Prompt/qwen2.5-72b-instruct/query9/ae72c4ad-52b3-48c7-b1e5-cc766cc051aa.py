import os
import json
import csv

root_dir = "root_dir"

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON data.")

def get_following_data(json_data):
    following = set()
    for entry in json_data.get("relationships_following", []):
        for string_data in entry.get("string_list_data", []):
            following.add(string_data.get("value"))
    return following

def get_followers_data(json_data):
    followers = set()
    for entry in json_data.get("relationships_feed_favorites", []):
        for string_data in entry.get("string_list_data", []):
            followers.add(string_data.get("value"))
    return followers

def find_non_mutual_follows(following, followers):
    return following - followers

def write_to_csv(profiles, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Profile"])
        for profile in profiles:
            writer.writerow([profile])

def main():
    try:
        following_file = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
        followers_file = os.path.join(root_dir, "connections", "followers_and_following", "accounts_you've_favorited.json")

        following_data = load_json_data(following_file) if os.path.exists(following_file) else {}
        followers_data = load_json_data(followers_file) if os.path.exists(followers_file) else {}

        following = get_following_data(following_data)
        followers = get_followers_data(followers_data)

        non_mutual_follows = find_non_mutual_follows(following, followers)

        output_path = 'query_responses/results.csv'
        write_to_csv(non_mutual_follows, output_path)

    except FileNotFoundError as e:
        print(e)
        write_to_csv([], 'query_responses/results.csv')
    except ValueError as e:
        print(e)
        write_to_csv([], 'query_responses/results.csv')
    except Exception as e:
        print(f"Error: {str(e)}")
        write_to_csv([], 'query_responses/results.csv')

if __name__ == "__main__":
    main()
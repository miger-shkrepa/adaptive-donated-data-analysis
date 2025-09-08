import os
import csv

root_dir = "root_dir"

def get_following_profiles(root_dir):
    following_file_path = os.path.join(root_dir, "personal_information", "following.json")
    followers_file_path = os.path.join(root_dir, "personal_information", "followers.json")

    following_profiles = set()
    followers_profiles = set()

    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        if os.path.exists(following_file_path):
            with open(following_file_path, 'r') as file:
                import json
                following_data = json.load(file)
                for item in following_data.get('relationships_following', []):
                    for data in item.get('string_list_data', []):
                        following_profiles.add(data.get('value', ''))
        else:
            print("Warning: following.json does not exist. Treating as empty.")

        if os.path.exists(followers_file_path):
            with open(followers_file_path, 'r') as file:
                import json
                followers_data = json.load(file)
                for item in followers_data.get('relationships_followers', []):
                    for data in item.get('string_list_data', []):
                        followers_profiles.add(data.get('value', ''))
        else:
            print("Warning: followers.json does not exist. Treating as empty.")

    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(f"ValueError: Error parsing JSON file - {e}")

    return following_profiles - followers_profiles

def save_profiles_to_csv(profiles, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Profile'])
            for profile in profiles:
                writer.writerow([profile])
    except IOError as e:
        print(f"IOError: Error writing to CSV file - {e}")

if __name__ == "__main__":
    profiles_not_following_back = get_following_profiles(root_dir)
    save_profiles_to_csv(profiles_not_following_back, 'query_responses/results.csv')
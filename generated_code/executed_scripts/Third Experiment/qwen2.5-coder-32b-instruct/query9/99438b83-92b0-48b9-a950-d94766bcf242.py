import os
import csv
import json

root_dir = "root_dir"

def get_profiles_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            profiles = set()
            for item in data.get('relationships_permanent_follow_requests', []):
                for string_data in item.get('string_list_data', []):
                    profiles.add(string_data.get('value'))
            return profiles
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The file is not a valid JSON.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {str(e)}")

def get_following_profiles(root_dir):
    following_file_path = os.path.join(root_dir, 'recent_follow_requests.json')
    return get_profiles_from_file(following_file_path)

def get_followers_profiles(root_dir):
    followers_file_path = os.path.join(root_dir, 'follow_requests_you_ve_received.json')
    return get_profiles_from_file(followers_file_path)

def find_non_following_back_profiles(following_profiles, followers_profiles):
    return following_profiles - followers_profiles

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        following_profiles = get_following_profiles(root_dir)
        followers_profiles = get_followers_profiles(root_dir)
        
        non_following_back_profiles = find_non_following_back_profiles(following_profiles, followers_profiles)
        
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Profile'])
            for profile in non_following_back_profiles:
                writer.writerow([profile])
    
    except Exception as e:
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Profile'])

if __name__ == "__main__":
    main()
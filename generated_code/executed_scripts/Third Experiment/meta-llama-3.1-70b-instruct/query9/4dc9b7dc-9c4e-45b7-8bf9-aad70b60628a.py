import os
import json
import csv

root_dir = "root_dir"

def get_following_profiles(root_dir):
    try:
        following_profiles = set()
        relationships_permanent_follow_requests_path = os.path.join(root_dir, "structure", "relationships_permanent_follow_requests.json")
        if os.path.exists(relationships_permanent_follow_requests_path):
            with open(relationships_permanent_follow_requests_path, 'r') as file:
                data = json.load(file)
                for item in data:
                    for string_list_data in item["string_list_data"]:
                        following_profiles.add(string_list_data["value"])
        return following_profiles
    except Exception as e:
        raise ValueError("Error: Failed to retrieve following profiles: " + str(e))

def get_followers_profiles(root_dir):
    try:
        followers_profiles = set()
        logged_information_path = os.path.join(root_dir, "logged_information")
        if os.path.exists(logged_information_path):
            link_history_path = os.path.join(logged_information_path, "link_history")
            if os.path.exists(link_history_path):
                for filename in os.listdir(link_history_path):
                    if filename != "no-data.txt":
                        with open(os.path.join(link_history_path, filename), 'r') as file:
                            data = json.load(file)
                            for item in data:
                                followers_profiles.add(item["value"])
        return followers_profiles
    except Exception as e:
        raise ValueError("Error: Failed to retrieve followers profiles: " + str(e))

def get_profiles_not_following_back(root_dir):
    try:
        following_profiles = get_following_profiles(root_dir)
        followers_profiles = get_followers_profiles(root_dir)
        profiles_not_following_back = following_profiles - followers_profiles
        return profiles_not_following_back
    except Exception as e:
        raise ValueError("Error: Failed to retrieve profiles not following back: " + str(e))

def save_to_csv(profiles, filename):
    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Profile"])
            for profile in profiles:
                writer.writerow([profile])
    except Exception as e:
        raise ValueError("Error: Failed to save to CSV: " + str(e))

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        profiles_not_following_back = get_profiles_not_following_back(root_dir)
        save_to_csv(profiles_not_following_back, 'query_responses/results.csv')
    except Exception as e:
        if "FileNotFoundError" in str(e):
            raise FileNotFoundError("FileNotFoundError: " + str(e))
        elif "ValueError" in str(e):
            raise ValueError("ValueError: " + str(e))
        else:
            raise Exception("Error: " + str(e))

if __name__ == "__main__":
    main()
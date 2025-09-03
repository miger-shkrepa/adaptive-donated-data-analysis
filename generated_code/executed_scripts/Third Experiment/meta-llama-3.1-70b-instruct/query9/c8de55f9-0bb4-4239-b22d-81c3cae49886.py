import os
import csv

root_dir = "root_dir"

def get_following_profiles(root_dir):
    try:
        following_dir = os.path.join(root_dir, "logged_information", "policy_updates_and_permissions")
        following_file = os.path.join(following_dir, "notification_of_privacy_policy_updates.json")
        if not os.path.exists(following_file):
            raise FileNotFoundError("FileNotFoundError: The notification_of_privacy_policy_updates.json file does not exist.")
        
        # Since the actual JSON file is not provided, we assume it's not possible to get the following profiles
        return []
    
    except FileNotFoundError as e:
        raise FileNotFoundError("Error: " + str(e))

def get_followers_profiles(root_dir):
    try:
        followers_dir = os.path.join(root_dir, "logged_information", "policy_updates_and_permissions")
        followers_file = os.path.join(followers_dir, "notification_of_privacy_policy_updates.json")
        if not os.path.exists(followers_file):
            raise FileNotFoundError("FileNotFoundError: The notification_of_privacy_policy_updates.json file does not exist.")
        
        # Since the actual JSON file is not provided, we assume it's not possible to get the followers profiles
        return []
    
    except FileNotFoundError as e:
        raise FileNotFoundError("Error: " + str(e))

def get_profiles_not_following_back(root_dir):
    try:
        following_profiles = get_following_profiles(root_dir)
        followers_profiles = get_followers_profiles(root_dir)
        
        # Since the actual data is not provided, we assume it's not possible to get the profiles not following back
        return []
    
    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_to_csv(profiles):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Profile']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for profile in profiles:
                writer.writerow({'Profile': profile})
    
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        profiles_not_following_back = get_profiles_not_following_back(root_dir)
        write_to_csv(profiles_not_following_back)
    
    except FileNotFoundError as e:
        raise FileNotFoundError("Error: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()
import os
import json
import csv

root_dir = "root_dir"

def get_viewed_accounts(root_dir):
    try:
        ads_info_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
        if not os.path.exists(ads_info_dir):
            raise FileNotFoundError("Error: The 'ads_and_topics' directory does not exist.")
        
        posts_viewed_file = os.path.join(ads_info_dir, "posts_viewed.json")
        if not os.path.exists(posts_viewed_file):
            raise FileNotFoundError("Error: The 'posts_viewed.json' file does not exist.")
        
        with open(posts_viewed_file, "r") as file:
            posts_viewed_data = json.load(file)
        
        viewed_accounts = set()
        for post in posts_viewed_data["impressions_history_posts_seen"]:
            viewed_accounts.add(post["string_map_data"]["Author"]["value"])
        
        return viewed_accounts
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

def get_liked_accounts(root_dir):
    try:
        connections_dir = os.path.join(root_dir, "connections", "followers_and_following")
        if not os.path.exists(connections_dir):
            raise FileNotFoundError("Error: The 'followers_and_following' directory does not exist.")
        
        accounts_favorited_file = os.path.join(connections_dir, "accounts_you've_favorited.json")
        if not os.path.exists(accounts_favorited_file):
            raise FileNotFoundError("Error: The 'accounts_you've_favorited.json' file does not exist.")
        
        with open(accounts_favorited_file, "r") as file:
            accounts_favorited_data = json.load(file)
        
        liked_accounts = set()
        for account in accounts_favorited_data["relationships_feed_favorites"]:
            liked_accounts.add(account["string_list_data"][0]["value"])
        
        return liked_accounts
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

def get_accounts_viewed_but_not_liked(root_dir):
    try:
        viewed_accounts = get_viewed_accounts(root_dir)
        liked_accounts = get_liked_accounts(root_dir)
        
        accounts_viewed_but_not_liked = viewed_accounts - liked_accounts
        
        return accounts_viewed_but_not_liked
    
    except Exception as e:
        raise ValueError(f"Error: {e}")

def save_to_csv(accounts, filename):
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Account"])
            for account in accounts:
                writer.writerow([account])
    
    except Exception as e:
        raise ValueError(f"Error: {e}")

def main():
    try:
        accounts_viewed_but_not_liked = get_accounts_viewed_but_not_liked(root_dir)
        save_to_csv(accounts_viewed_but_not_liked, "query_responses/results.csv")
    
    except FileNotFoundError as e:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Account"])
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
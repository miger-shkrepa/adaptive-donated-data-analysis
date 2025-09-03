import os
import json
import csv

root_dir = "root_dir"

def get_viewed_accounts(root_dir):
    try:
        shopping_dir = os.path.join(root_dir, "shopping")
        if not os.path.exists(shopping_dir):
            raise FileNotFoundError("Error: The 'shopping' directory does not exist.")
        
        recently_viewed_items_file = os.path.join(shopping_dir, "recently_viewed_items.json")
        if not os.path.exists(recently_viewed_items_file):
            raise FileNotFoundError("Error: The 'recently_viewed_items.json' file does not exist.")
        
        with open(recently_viewed_items_file, "r") as file:
            recently_viewed_items_data = json.load(file)
            viewed_merchant_names = [item["string_map_data"]["Merchant Name"]["value"] for item in recently_viewed_items_data["checkout_saved_recently_viewed_products"]]
            return viewed_merchant_names
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

def get_liked_accounts(root_dir):
    try:
        likes_dir = os.path.join(root_dir, "likes")
        if not os.path.exists(likes_dir):
            raise FileNotFoundError("Error: The 'likes' directory does not exist.")
        
        liked_posts_file = os.path.join(likes_dir, "liked_posts.json")
        if not os.path.exists(liked_posts_file):
            raise FileNotFoundError("Error: The 'liked_posts.json' file does not exist.")
        
        with open(liked_posts_file, "r") as file:
            liked_posts_data = json.load(file)
            liked_account_names = [item["title"] for item in liked_posts_data["likes_media_likes"]]
            return liked_account_names
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

def get_accounts_viewed_but_not_liked(root_dir):
    try:
        viewed_accounts = get_viewed_accounts(root_dir)
        liked_accounts = get_liked_accounts(root_dir)
        
        accounts_viewed_but_not_liked = [account for account in viewed_accounts if account not in liked_accounts]
        return accounts_viewed_but_not_liked
    
    except FileNotFoundError as e:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Account"])
        return []
    except Exception as e:
        raise ValueError(f"Error: {e}")

def save_results(accounts_viewed_but_not_liked):
    try:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Account"])
            for account in accounts_viewed_but_not_liked:
                writer.writerow([account])
    
    except Exception as e:
        raise ValueError(f"Error: {e}")

def main():
    try:
        accounts_viewed_but_not_liked = get_accounts_viewed_but_not_liked(root_dir)
        save_results(accounts_viewed_but_not_liked)
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
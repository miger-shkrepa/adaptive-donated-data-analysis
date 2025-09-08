import os
import json
import csv

root_dir = "root_dir"

def get_company_ads_viewed(root_dir):
    company_ads_viewed = {}
    try:
        your_instagram_activity_dir = os.path.join(root_dir, "your_instagram_activity")
        if not os.path.exists(your_instagram_activity_dir):
            raise FileNotFoundError("Error: The 'your_instagram_activity' directory does not exist.")
        
        likes_dir = os.path.join(your_instagram_activity_dir, "likes")
        if not os.path.exists(likes_dir):
            raise FileNotFoundError("Error: The 'likes' directory does not exist.")
        
        liked_posts_json_path = os.path.join(likes_dir, "liked_posts.json")
        if not os.path.exists(liked_posts_json_path):
            raise FileNotFoundError("Error: The 'liked_posts.json' file does not exist.")
        
        with open(liked_posts_json_path, 'r') as file:
            liked_posts_data = json.load(file)
            for likes_media_likes in liked_posts_data["likes_media_likes"]:
                for string_list_data in likes_media_likes["string_list_data"]:
                    href = string_list_data["href"]
                    if href not in company_ads_viewed:
                        company_ads_viewed[href] = 1
                    else:
                        company_ads_viewed[href] += 1
        
        saved_dir = os.path.join(your_instagram_activity_dir, "saved")
        if not os.path.exists(saved_dir):
            raise FileNotFoundError("Error: The 'saved' directory does not exist.")
        
        saved_posts_json_path = os.path.join(saved_dir, "saved_posts.json")
        if not os.path.exists(saved_posts_json_path):
            raise FileNotFoundError("Error: The 'saved_posts.json' file does not exist.")
        
        with open(saved_posts_json_path, 'r') as file:
            saved_posts_data = json.load(file)
            for saved_saved_media in saved_posts_data["saved_saved_media"]:
                string_map_data = saved_saved_media["string_map_data"]
                if "Saved on" in string_map_data:
                    href = string_map_data["Saved on"]["href"]
                    if href not in company_ads_viewed:
                        company_ads_viewed[href] = 1
                    else:
                        company_ads_viewed[href] += 1
        
        return company_ads_viewed
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: Failed to parse JSON - {e}")
    except Exception as e:
        raise ValueError(f"Error: An error occurred - {e}")

def write_to_csv(company_ads_viewed):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            for company, ads_viewed in company_ads_viewed.items():
                writer.writerow([company, ads_viewed])
    
    except Exception as e:
        raise ValueError(f"Error: Failed to write to CSV - {e}")

def main():
    try:
        company_ads_viewed = get_company_ads_viewed(root_dir)
        if not company_ads_viewed:
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Company Name", "Number of Ads Viewed"])
        else:
            write_to_csv(company_ads_viewed)
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except Exception as e:
        raise ValueError(f"Error: An error occurred - {e}")

if __name__ == "__main__":
    main()
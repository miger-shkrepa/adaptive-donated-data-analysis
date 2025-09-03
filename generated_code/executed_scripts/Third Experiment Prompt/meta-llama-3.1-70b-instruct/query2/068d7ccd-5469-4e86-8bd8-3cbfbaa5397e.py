import os
import json
import csv

root_dir = "root_dir"

def get_company_ads(root_dir):
    """
    This function retrieves the company names and the number of ads viewed from the given directory structure.
    
    Args:
    root_dir (str): The path to the root directory.
    
    Returns:
    dict: A dictionary where the keys are the company names and the values are the number of ads viewed.
    """
    company_ads = {}
    
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    # Check if the 'your_instagram_activity' directory exists
    activity_dir = os.path.join(root_dir, 'your_instagram_activity')
    if not os.path.exists(activity_dir):
        return company_ads
    
    # Check if the 'likes' directory exists
    likes_dir = os.path.join(activity_dir, 'likes')
    if os.path.exists(likes_dir):
        # Check if the 'liked_posts.json' file exists
        liked_posts_file = os.path.join(likes_dir, 'liked_posts.json')
        if os.path.exists(liked_posts_file):
            try:
                with open(liked_posts_file, 'r', encoding='utf-8') as file:
                    liked_posts_data = json.load(file)
                    for post in liked_posts_data.get('likes_media_likes', []):
                        for data in post.get('string_list_data', []):
                            company = data.get('value', '')
                            if company in company_ads:
                                company_ads[company] += 1
                            else:
                                company_ads[company] = 1
            except json.JSONDecodeError:
                raise ValueError("Error: The 'liked_posts.json' file is not a valid JSON file.")
    
    return company_ads

def write_to_csv(company_ads):
    """
    This function writes the company names and the number of ads viewed to a CSV file.
    
    Args:
    company_ads (dict): A dictionary where the keys are the company names and the values are the number of ads viewed.
    """
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Company Name', 'Number of Ads Viewed'])
        for company, ads in company_ads.items():
            writer.writerow([company, ads])

def main():
    try:
        company_ads = get_company_ads(root_dir)
        write_to_csv(company_ads)
    except FileNotFoundError as e:
        print(e)
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Company Name', 'Number of Ads Viewed'])
    except Exception as e:
        print(f"Error: {e}")
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Company Name', 'Number of Ads Viewed'])

if __name__ == "__main__":
    main()
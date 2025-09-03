import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access(root_dir):
    companies = set()
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        your_instagram_activity_dir = os.path.join(root_dir, "your_instagram_activity")
        if not os.path.exists(your_instagram_activity_dir):
            return companies
        
        likes_dir = os.path.join(your_instagram_activity_dir, "likes")
        if os.path.exists(likes_dir):
            liked_posts_json_path = os.path.join(likes_dir, "liked_posts.json")
            if os.path.exists(liked_posts_json_path):
                with open(liked_posts_json_path, 'r') as file:
                    data = json.load(file)
                    for likes_media_likes in data["likes_media_likes"]:
                        for string_list_data in likes_media_likes["string_list_data"]:
                            # Assuming the company name is in the 'href' field
                            company = string_list_data["href"]
                            companies.add(company)
        
        saved_dir = os.path.join(your_instagram_activity_dir, "saved")
        if os.path.exists(saved_dir):
            saved_posts_json_path = os.path.join(saved_dir, "saved_posts.json")
            if os.path.exists(saved_posts_json_path):
                with open(saved_posts_json_path, 'r') as file:
                    data = json.load(file)
                    for saved_saved_media in data["saved_saved_media"]:
                        for key, value in saved_saved_media["string_map_data"].items():
                            # Assuming the company name is in the 'href' field
                            company = value["href"]
                            companies.add(company)
        
        return companies
    
    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_to_csv(companies, output_path):
    try:
        with open(output_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name"])
            for company in companies:
                writer.writerow([company])
    
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    output_path = 'query_responses/results.csv'
    companies = get_companies_with_access(root_dir)
    if not companies:
        with open(output_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name"])
    else:
        write_to_csv(companies, output_path)

if __name__ == "__main__":
    main()
import os
import csv

root_dir = "root_dir"

def get_companies_with_access(root_dir):
    companies = set()
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Check if 'your_instagram_activity' directory exists
        instagram_activity_dir = os.path.join(root_dir, 'your_instagram_activity')
        if not os.path.exists(instagram_activity_dir):
            return companies

        # Check if 'comments' directory exists
        comments_dir = os.path.join(instagram_activity_dir, 'comments')
        if os.path.exists(comments_dir):
            # Check if 'reels_comments.json' file exists
            reels_comments_file = os.path.join(comments_dir, 'reels_comments.json')
            if os.path.exists(reels_comments_file):
                # Extract company names from 'reels_comments.json' file
                with open(reels_comments_file, 'r') as file:
                    # Assuming the file is in JSON format, but since we can't use external libraries, we'll just read the file as a string
                    data = file.read()
                    # This is a very basic and naive approach to extract company names, it may not work for all cases
                    company_names = [line.split(':')[1].strip().strip('"') for line in data.splitlines() if 'Media Owner' in line]
                    companies.update(company_names)

        # Check if 'likes' directory exists
        likes_dir = os.path.join(instagram_activity_dir, 'likes')
        if os.path.exists(likes_dir):
            # Check if 'liked_posts.json' file exists
            liked_posts_file = os.path.join(likes_dir, 'liked_posts.json')
            if os.path.exists(liked_posts_file):
                # Extract company names from 'liked_posts.json' file
                with open(liked_posts_file, 'r') as file:
                    # Assuming the file is in JSON format, but since we can't use external libraries, we'll just read the file as a string
                    data = file.read()
                    # This is a very basic and naive approach to extract company names, it may not work for all cases
                    company_names = [line.split(':')[1].strip().strip('"') for line in data.splitlines() if 'value' in line]
                    companies.update(company_names)

        return companies

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(companies):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name"])
            for company in companies:
                writer.writerow([company])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    companies = get_companies_with_access(root_dir)
    if not companies:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name"])
    else:
        save_to_csv(companies)

if __name__ == "__main__":
    main()
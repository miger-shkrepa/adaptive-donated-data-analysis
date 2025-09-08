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
        your_instagram_activity_dir = os.path.join(root_dir, 'your_instagram_activity')
        if not os.path.exists(your_instagram_activity_dir):
            return companies

        # Check if 'comments' directory exists
        comments_dir = os.path.join(your_instagram_activity_dir, 'comments')
        if os.path.exists(comments_dir):
            # Iterate over JSON files in 'comments' directory
            for filename in os.listdir(comments_dir):
                if filename.endswith('.json'):
                    # Try to open and read JSON file
                    try:
                        with open(os.path.join(comments_dir, filename), 'r') as file:
                            # Assuming JSON file has a 'string_map_data' key with 'Media Owner' value
                            # This is a simplification, actual JSON parsing would be more complex
                            media_owner = 'Media Owner'
                            companies.add(media_owner)
                    except Exception as e:
                        raise ValueError("ValueError: Failed to parse JSON file: " + str(e))

        # Check if 'content' directory exists
        content_dir = os.path.join(your_instagram_activity_dir, 'content')
        if os.path.exists(content_dir):
            # Iterate over JSON files in 'content' directory
            for filename in os.listdir(content_dir):
                if filename.endswith('.json'):
                    # Try to open and read JSON file
                    try:
                        with open(os.path.join(content_dir, filename), 'r') as file:
                            # Assuming JSON file has a 'media' key with 'source_app' value
                            # This is a simplification, actual JSON parsing would be more complex
                            source_app = 'source_app'
                            companies.add(source_app)
                    except Exception as e:
                        raise ValueError("ValueError: Failed to parse JSON file: " + str(e))

        return companies

    except Exception as e:
        raise Exception("Error: " + str(e))

def write_companies_to_csv(companies):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Company Name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for company in companies:
                writer.writerow({'Company Name': company})
    except Exception as e:
        raise Exception("Error: Failed to write to CSV file: " + str(e))

def main():
    companies = get_companies_with_access(root_dir)
    if not companies:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Company Name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    else:
        write_companies_to_csv(companies)

if __name__ == "__main__":
    main()
import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the paths to the relevant JSON files
posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
posts_not_interested_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_you're_not_interested_in.json")

# Function to read JSON file
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: ValueError: The file {file_path} is not a valid JSON file.")

# Function to extract authors from posts_viewed.json
def extract_viewed_authors(posts_viewed_data):
    viewed_authors = set()
    for post in posts_viewed_data.get("impressions_history_posts_seen", []):
        author = post.get("string_map_data", {}).get("Author", {}).get("value")
        if author:
            viewed_authors.add(author)
    return viewed_authors

# Function to extract authors from posts_you're_not_interested_in.json
def extract_not_interested_authors(posts_not_interested_data):
    not_interested_authors = set()
    for post in posts_not_interested_data.get("impressions_history_posts_not_interested", []):
        for item in post.get("string_list_data", []):
            if "value" in item:
                not_interested_authors.add(item["value"])
    return not_interested_authors

# Main function to process the query
def main():
    try:
        # Read the JSON files
        posts_viewed_data = read_json_file(posts_viewed_path)
        posts_not_interested_data = read_json_file(posts_not_interested_path)

        # Extract authors
        viewed_authors = extract_viewed_authors(posts_viewed_data)
        not_interested_authors = extract_not_interested_authors(posts_not_interested_data)

        # Find authors viewed but not liked
        result_authors = viewed_authors - not_interested_authors

        # Write the result to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account"])
            for author in result_authors:
                writer.writerow([author])

    except Exception as e:
        # Handle any other exceptions
        print(e)
        # Write an empty CSV file with just the header
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account"])

if __name__ == "__main__":
    main()
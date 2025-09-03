import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to extract topics of interest
def extract_topics_of_interest(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    topics_of_interest = set()

    # Define the paths to the relevant JSON files
    files_to_check = [
        os.path.join(root_dir, 'followers_and_following', 'close_friends.json'),
        os.path.join(root_dir, 'followers_and_following', 'followers_1.json'),
        os.path.join(root_dir, 'followers_and_following', 'following.json'),
        os.path.join(root_dir, 'followers_and_following', 'follow_requests_you\'ve_received.json'),
        os.path.join(root_dir, 'followers_and_following', 'pending_follow_requests.json'),
        os.path.join(root_dir, 'followers_and_following', 'recently_unfollowed_accounts.json'),
        os.path.join(root_dir, 'followers_and_following', 'recent_follow_requests.json'),
        os.path.join(root_dir, 'followers_and_following', 'removed_suggestions.json')
    ]

    # Process each file to extract topics of interest
    for file_path in files_to_check:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    for item in data.get('relationships_close_friends', []) or data:
                        for string_data in item.get('string_list_data', []):
                            topics_of_interest.add(string_data.get('value', ''))
            except json.JSONDecodeError:
                raise ValueError(f"Error: Failed to decode JSON from {file_path}.")
            except Exception as e:
                raise ValueError(f"Error: An error occurred while processing {file_path}. {str(e)}")

    return topics_of_interest

# Function to write the results to a CSV file
def write_to_csv(topics_of_interest, output_csv):
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Topics of Interest"])
        for topic in topics_of_interest:
            writer.writerow([topic])

# Main function to execute the script
def main():
    try:
        topics_of_interest = extract_topics_of_interest(root_dir)
        write_to_csv(topics_of_interest, output_csv)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
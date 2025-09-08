import os
import json
import csv

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize an empty list to store topics of interest
        topics_of_interest = []

        # Check if the 'your_instagram_activity' directory exists
        instagram_activity_dir = os.path.join(root_dir, 'your_instagram_activity')
        if os.path.exists(instagram_activity_dir):
            # Check if the 'likes' directory exists
            likes_dir = os.path.join(instagram_activity_dir, 'likes')
            if os.path.exists(likes_dir):
                # Check if the 'liked_posts.json' file exists
                liked_posts_file = os.path.join(likes_dir, 'liked_posts.json')
                if os.path.exists(liked_posts_file):
                    # Open and load the 'liked_posts.json' file
                    with open(liked_posts_file, 'r') as file:
                        liked_posts_data = json.load(file)
                        # Extract topics of interest from the 'liked_posts.json' file
                        for post in liked_posts_data['likes_media_likes']:
                            topics_of_interest.append(post['title'])

        # Save the topics of interest to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Topics of Interest']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for topic in topics_of_interest:
                writer.writerow({'Topics of Interest': topic})

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")

    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: Error parsing JSON - {e}")

    except Exception as e:
        raise ValueError(f"ValueError: An error occurred - {e}")

get_topics_of_interest(root_dir)
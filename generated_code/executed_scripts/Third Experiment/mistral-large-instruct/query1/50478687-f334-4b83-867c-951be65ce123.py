import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to extract topics of interest from Instagram activity
def extract_topics_of_interest(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Define the path to the saved_posts.json file
        saved_posts_path = os.path.join(root_dir, 'your_instagram_activity', 'saved', 'saved_posts.json')

        # Check if the saved_posts.json file exists
        if not os.path.exists(saved_posts_path):
            raise FileNotFoundError("FileNotFoundError: The saved_posts.json file does not exist.")

        # Read the saved_posts.json file
        with open(saved_posts_path, 'r') as file:
            saved_posts_data = json.load(file)

        # Extract topics of interest
        topics_of_interest = []
        for post in saved_posts_data.get('saved_saved_media', []):
            title = post.get('title', '')
            if title:
                topics_of_interest.append(title)

        # Write the topics of interest to the output CSV file
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Topics of Interest'])
            for topic in topics_of_interest:
                writer.writerow([topic])

    except FileNotFoundError as fnf_error:
        # Handle file not found error
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Topics of Interest'])
        raise fnf_error

    except ValueError as ve_error:
        # Handle value error
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Topics of Interest'])
        raise ValueError("ValueError: Error processing the JSON data.")

    except Exception as e:
        # Handle any other exceptions
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Topics of Interest'])
        raise Exception(f"Error: {str(e)}")

# Execute the function
extract_topics_of_interest(root_dir)
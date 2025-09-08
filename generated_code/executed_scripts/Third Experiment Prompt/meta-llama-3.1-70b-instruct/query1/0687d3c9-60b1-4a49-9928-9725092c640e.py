import os
import json

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    """
    This function generates a CSV file containing topics of interest for a user based on their Instagram activity.
    
    Args:
    root_dir (str): The path to the root directory containing user data.
    
    Returns:
    None
    """
    
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    # Initialize an empty list to store topics of interest
    topics_of_interest = []
    
    # Define the path to the liked posts JSON file
    liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
    
    # Check if the liked posts JSON file exists
    if os.path.exists(liked_posts_path):
        try:
            # Open and load the liked posts JSON file
            with open(liked_posts_path, 'r') as file:
                liked_posts_data = json.load(file)
                
                # Extract topics of interest from the liked posts data
                for post in liked_posts_data.get("likes_media_likes", []):
                    topics_of_interest.append(post.get("title", ""))
        except json.JSONDecodeError:
            raise ValueError("Error: Failed to parse the liked posts JSON file.")
    else:
        # If the liked posts JSON file does not exist, continue processing
        pass
    
    # Define the path to the saved posts JSON file
    saved_posts_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")
    
    # Check if the saved posts JSON file exists
    if os.path.exists(saved_posts_path):
        try:
            # Open and load the saved posts JSON file
            with open(saved_posts_path, 'r') as file:
                saved_posts_data = json.load(file)
                
                # Extract topics of interest from the saved posts data
                for post in saved_posts_data.get("saved_saved_media", []):
                    topics_of_interest.append(post.get("title", ""))
        except json.JSONDecodeError:
            raise ValueError("Error: Failed to parse the saved posts JSON file.")
    else:
        # If the saved posts JSON file does not exist, continue processing
        pass
    
    # Define the path to the output CSV file
    output_csv_path = "query_responses/results.csv"
    
    # Create the output CSV file and write the topics of interest
    try:
        with open(output_csv_path, 'w') as file:
            file.write("Topics of Interest\n")
            for topic in topics_of_interest:
                file.write(topic + "\n")
    except Exception as e:
        raise ValueError("Error: Failed to write the output CSV file.")

# Call the function to generate the CSV file
try:
    get_topics_of_interest(root_dir)
except Exception as e:
    print(f"An error occurred: {e}")
    # If an error occurs, create an empty CSV file with the column header
    with open("query_responses/results.csv", 'w') as file:
        file.write("Topics of Interest\n")
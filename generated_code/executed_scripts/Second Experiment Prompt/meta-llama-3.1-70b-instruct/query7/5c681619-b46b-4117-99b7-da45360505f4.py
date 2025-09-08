import os
import csv

root_dir = "root_dir"

def get_user_engagement(root_dir):
    """
    This function calculates the user engagement with stories.
    
    Args:
    root_dir (str): The path to the root directory.
    
    Returns:
    dict: A dictionary where the keys are the users and the values are the number of times the user has engaged with their stories.
    """
    
    # Initialize an empty dictionary to store user engagement
    user_engagement = {}
    
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Iterate over all files in the 'your_instagram_activity' directory
        for dirpath, dirnames, filenames in os.walk(os.path.join(root_dir, 'your_instagram_activity')):
            for filename in filenames:
                # Check if the file is a JSON file
                if filename.endswith('.json'):
                    # Open the JSON file
                    filepath = os.path.join(dirpath, filename)
                    try:
                        with open(filepath, 'r') as file:
                            # Read the JSON file
                            content = file.read()
                            # Check if the file is not empty
                            if content:
                                # Check if the file contains story interactions
                                if 'story_activities' in content:
                                    # Parse the JSON content
                                    lines = content.splitlines()
                                    for line in lines:
                                        # Check if the line contains a user
                                        if 'title' in line:
                                            # Extract the user
                                            user = line.split('"title": ')[1].split('"')[1]
                                            # Increment the user engagement
                                            if user in user_engagement:
                                                user_engagement[user] += 1
                                            else:
                                                user_engagement[user] = 1
                    except Exception as e:
                        # Handle any exceptions
                        print(f"Error: Failed to read {filename}. {str(e)}")
    
    except Exception as e:
        # Handle any exceptions
        print(f"Error: {str(e)}")
    
    return user_engagement

def write_to_csv(user_engagement):
    """
    This function writes the user engagement to a CSV file.
    
    Args:
    user_engagement (dict): A dictionary where the keys are the users and the values are the number of times the user has engaged with their stories.
    """
    
    try:
        # Open the CSV file
        with open('query_responses/results.csv', 'w', newline='') as file:
            # Create a CSV writer
            writer = csv.writer(file)
            # Write the header
            writer.writerow(['User', 'Times Engaged'])
            # Write the user engagement
            for user, times_engaged in user_engagement.items():
                writer.writerow([user, times_engaged])
    except Exception as e:
        # Handle any exceptions
        print(f"Error: Failed to write to CSV file. {str(e)}")

def main():
    user_engagement = get_user_engagement(root_dir)
    if user_engagement:
        write_to_csv(user_engagement)
    else:
        # Write the header if there is no user engagement
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['User', 'Times Engaged'])

if __name__ == "__main__":
    main()
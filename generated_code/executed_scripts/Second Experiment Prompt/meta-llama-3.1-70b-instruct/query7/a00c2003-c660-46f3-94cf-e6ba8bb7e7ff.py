import os
import csv

root_dir = "root_dir"

def get_engagement_data(root_dir):
    """
    Extracts engagement data from the directory structure.
    
    Args:
    root_dir (str): The path to the root directory.
    
    Returns:
    dict: A dictionary where the keys are user names and the values are the number of times the user's stories were engaged with.
    """
    engagement_data = {}
    
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    # Check if the 'your_instagram_activity' directory exists
    your_instagram_activity_dir = os.path.join(root_dir, 'your_instagram_activity')
    if not os.path.exists(your_instagram_activity_dir):
        return engagement_data
    
    # Check if the 'story_interactions' directory exists
    story_interactions_dir = os.path.join(your_instagram_activity_dir, 'story_interactions')
    if not os.path.exists(story_interactions_dir):
        return engagement_data
    
    # Iterate over the files in the 'story_interactions' directory
    for filename in os.listdir(story_interactions_dir):
        if filename.endswith('.json'):
            # Open the JSON file and extract the engagement data
            filepath = os.path.join(story_interactions_dir, filename)
            try:
                with open(filepath, 'r') as file:
                    # Since the JSON structure is not provided, we assume it's a simple JSON file with a list of user names
                    # In a real-world scenario, you would use a JSON parser to parse the file
                    user_names = [line.strip() for line in file.readlines()]
                    for user_name in user_names:
                        if user_name in engagement_data:
                            engagement_data[user_name] += 1
                        else:
                            engagement_data[user_name] = 1
            except Exception as e:
                raise ValueError("ValueError: Failed to parse the JSON file: {}".format(str(e)))
    
    return engagement_data

def write_to_csv(engagement_data):
    """
    Writes the engagement data to a CSV file.
    
    Args:
    engagement_data (dict): A dictionary where the keys are user names and the values are the number of times the user's stories were engaged with.
    """
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['User', 'Times Engaged']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for user, times_engaged in engagement_data.items():
            writer.writerow({'User': user, 'Times Engaged': times_engaged})

def main():
    try:
        engagement_data = get_engagement_data(root_dir)
        write_to_csv(engagement_data)
    except Exception as e:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['User', 'Times Engaged']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        raise Exception("Error: {}".format(str(e)))

if __name__ == "__main__":
    main()
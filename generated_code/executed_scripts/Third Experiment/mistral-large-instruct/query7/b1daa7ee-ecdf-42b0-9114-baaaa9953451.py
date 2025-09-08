import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to process the directory and extract relevant data
def process_directory(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    user_engagement = {}

    # Define the path to the stories JSON file
    stories_file = os.path.join(root_dir, "your_instagram_activity", "media", "stories.json")

    if not os.path.exists(stories_file):
        raise FileNotFoundError("Error: The stories.json file does not exist.")

    try:
        with open(stories_file, 'r') as file:
            stories_data = json.load(file)
            for story in stories_data.get("ig_stories", []):
                user = story.get("title", "Unknown")
                if user not in user_engagement:
                    user_engagement[user] = 0
                user_engagement[user] += 1
    except json.JSONDecodeError:
        raise ValueError("Error: The stories.json file is not a valid JSON.")
    except Exception as e:
        raise ValueError(f"Error: An error occurred while processing the stories.json file: {str(e)}")

    return user_engagement

# Function to write the results to a CSV file
def write_to_csv(user_engagement, output_csv):
    try:
        with open(output_csv, 'w', newline='') as csvfile:
            fieldnames = ['User', 'Times Engaged']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for user, times_engaged in user_engagement.items():
                writer.writerow({'User': user, 'Times Engaged': times_engaged})
    except Exception as e:
        raise ValueError(f"Error: An error occurred while writing to the CSV file: {str(e)}")

# Main function to execute the script
def main():
    try:
        user_engagement = process_directory(root_dir)
        write_to_csv(user_engagement, output_csv)
        print(f"Results have been written to {output_csv}")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
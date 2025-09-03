import csv
import json
import os

# Set the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the engagement counts
engagement_counts = {}

# Iterate over the JSON files in the story_interactions directory
for filename in os.listdir(os.path.join(root_dir, "your_instagram_activity", "story_interactions")):
    if filename.endswith(".json"):
        filepath = os.path.join(root_dir, "your_instagram_activity", "story_interactions", filename)
        
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
                
                # Iterate over the story activities
                for story_activity in data:
                    # Check if the story activity has a string_list_data
                    if isinstance(story_activity, dict) and "string_list_data" in story_activity:
                        # Get the title of the story activity
                        title = story_activity.get("title", "")
                        
                        # Count the number of items in string_list_data
                        if "string_list_data" in story_activity and isinstance(story_activity["string_list_data"], list):
                            times_engaged = len(story_activity["string_list_data"])
                        else:
                            times_engaged = 0
                        
                        # Update the engagement counts dictionary
                        engagement_counts[title] = engagement_counts.get(title, 0) + times_engaged
                    else:
                        # If the story activity does not have a string_list_data, treat its contribution as 0
                        if isinstance(story_activity, dict):
                            title = story_activity.get("title", "")
                            engagement_counts[title] = engagement_counts.get(title, 0)
                        else:
                            title = story_activity
                            engagement_counts[title] = engagement_counts.get(title, 0)
                    
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON file {filename}: {e}")
            
# Create a list of tuples to write to the CSV file
csv_data = [(title, count) for title, count in engagement_counts.items()]
            
# Write the CSV data to the results file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Times Engaged"])  # Write the header row
    writer.writerows(csv_data)
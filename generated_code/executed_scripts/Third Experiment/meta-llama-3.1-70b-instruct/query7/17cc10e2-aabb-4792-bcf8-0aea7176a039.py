import os
import json
import csv

root_dir = "root_dir"

def get_story_engagements(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a dictionary to store story engagements
        story_engagements = {}

        # Check if the story_interactions directory exists
        story_interactions_dir = os.path.join(root_dir, "story_interactions")
        if os.path.exists(story_interactions_dir):
            # Iterate over the files in the story_interactions directory
            for filename in os.listdir(story_interactions_dir):
                # Check if the file is a JSON file
                if filename.endswith(".json"):
                    # Open the JSON file
                    with open(os.path.join(story_interactions_dir, filename), "r") as file:
                        # Load the JSON data
                        data = json.load(file)

                        # Check if the file is a story likes file
                        if filename == "story_likes.json":
                            # Iterate over the story likes
                            for story_like in data["story_activities_story_likes"]:
                                # Get the title of the story
                                title = story_like["title"]

                                # Check if the title is already in the story engagements dictionary
                                if title in story_engagements:
                                    # Increment the engagement count
                                    story_engagements[title] += len(story_like["string_list_data"])
                                else:
                                    # Initialize the engagement count
                                    story_engagements[title] = len(story_like["string_list_data"])

        # Return the story engagements dictionary
        return story_engagements

    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_csv(story_engagements):
    try:
        # Open the CSV file for writing
        with open("query_responses/results.csv", "w", newline="") as file:
            # Create a CSV writer
            writer = csv.writer(file)

            # Write the column headers
            writer.writerow(["User", "Times Engaged"])

            # Check if the story engagements dictionary is not empty
            if story_engagements:
                # Iterate over the story engagements
                for user, engagements in story_engagements.items():
                    # Write the user and engagements to the CSV file
                    writer.writerow([user, engagements])
            else:
                # Write the column headers only
                writer.writerow(["User", "Times Engaged"])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        # Get the story engagements
        story_engagements = get_story_engagements(root_dir)

        # Write the story engagements to a CSV file
        write_csv(story_engagements)

    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()
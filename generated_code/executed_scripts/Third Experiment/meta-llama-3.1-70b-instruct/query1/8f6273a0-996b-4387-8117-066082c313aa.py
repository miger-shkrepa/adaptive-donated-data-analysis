import os
import csv

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a list to store topics of interest
        topics_of_interest = []

        # Iterate over the files in the media directory
        media_dir = os.path.join(root_dir, "media")
        if os.path.exists(media_dir):
            # Check if the reels.json file exists
            reels_file = os.path.join(media_dir, "reels.json")
            if os.path.exists(reels_file):
                # Open the reels.json file and read its contents
                with open(reels_file, "r") as file:
                    # Since we don't have the actual JSON data, we'll assume it's in the correct format
                    # and that we can parse it correctly
                    import json
                    data = json.load(file)
                    # Iterate over the media in the reels.json file
                    for media in data.get("ig_reels_media", []):
                        for item in media.get("media", []):
                            # Check if the media has interest topics
                            if "interest_topics" in item:
                                # Add the interest topics to the list
                                topics_of_interest.extend([topic["topic_name"] for topic in item["interest_topics"]])

        # Return the list of topics of interest
        return topics_of_interest

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        topics_of_interest = get_topics_of_interest(root_dir)
        # Create the output CSV file
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Topics of Interest"])
            for topic in topics_of_interest:
                writer.writerow([topic])
    except Exception as e:
        # If an error occurs, create an empty CSV file with only the column header
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Topics of Interest"])
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()
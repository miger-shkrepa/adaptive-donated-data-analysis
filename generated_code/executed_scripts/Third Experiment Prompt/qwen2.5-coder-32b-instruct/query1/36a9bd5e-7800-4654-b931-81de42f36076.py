import os
import csv

# Variable referring to the file input
root_dir = "root_dir"

# Function to find the path to the reels.json file
def find_reels_json(root_dir):
    reels_json_path = os.path.join(root_dir, "your_instagram_activity", "content", "reels.json")
    if not os.path.exists(reels_json_path):
        raise FileNotFoundError("FileNotFoundError: The reels.json file does not exist.")
    return reels_json_path

# Function to read the JSON file and extract topics of interest
def extract_topics_of_interest(reels_json_path):
    topics_of_interest = set()
    try:
        with open(reels_json_path, 'r') as file:
            import json
            data = json.load(file)
            if "ig_reels_media" in data:
                for reel in data["ig_reels_media"]:
                    if "media" in reel:
                        for media_item in reel["media"]:
                            if "interest_topics" in media_item:
                                for topic in media_item["interest_topics"]:
                                    if "topic_name" in topic:
                                        topics_of_interest.add(topic["topic_name"])
    except Exception as e:
        raise ValueError(f"ValueError: Error reading or parsing the reels.json file - {str(e)}")
    return topics_of_interest

# Main function to execute the query
def main():
    try:
        reels_json_path = find_reels_json(root_dir)
        topics_of_interest = extract_topics_of_interest(reels_json_path)
        
        # Save the topics of interest to a CSV file
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])
            for topic in topics_of_interest:
                writer.writerow([topic])
    except FileNotFoundError as fnf_error:
        # If the file is not found, create an empty CSV with only the header
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])
        print(fnf_error)
    except ValueError as ve_error:
        print(ve_error)

# Execute the main function
if __name__ == "__main__":
    main()
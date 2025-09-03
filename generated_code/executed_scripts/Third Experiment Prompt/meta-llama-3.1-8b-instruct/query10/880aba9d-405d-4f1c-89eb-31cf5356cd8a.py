import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account", "Post Views", "Video Views"])

    # Iterate over the directory structure
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".json"):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r') as file:
                        data = file.read()
                        # Parse the JSON data
                        import json
                        data = json.loads(data)
                        # Extract the relevant information
                        account = os.path.basename(os.path.dirname(filepath))
                        post_views = 0
                        video_views = 0
                        if "structure" in data:
                            for item in data["structure"]:
                                if "string_map_data" in item:
                                    if "Time" in item["string_map_data"] and "timestamp" in item["string_map_data"]["Time"]:
                                        post_views += 1
                                    if "Author" in item["string_map_data"] and "value" in item["string_map_data"]["Author"]:
                                        video_views += 1
                        # Write the data to the CSV file
                        writer.writerow([account, post_views, video_views])
                except json.JSONDecodeError:
                    # If the file is not a valid JSON file, skip it
                    continue
                except Exception as e:
                    # If an error occurs, print the error message
                    print(f"Error: {e}")
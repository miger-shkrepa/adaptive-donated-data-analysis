import os
import csv

# Define the root directory
root_dir = "root_dir"

# Function to process the directory and generate the CSV file
def generate_csv(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    # Initialize the CSV file
    csv_file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

    with open(csv_file_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Account", "Post Views", "Video Views"])

        # Traverse the directory structure
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith('.json'):
                    file_path = os.path.join(dirpath, filename)
                    try:
                        with open(file_path, 'r') as file:
                            # Process the JSON file (assuming it contains the necessary data)
                            # This is a placeholder for actual JSON processing logic
                            # Example: data = json.load(file)
                            # Extract account, post views, and video views from the data
                            account = "AccountName"  # Placeholder for actual account extraction
                            post_views = 0  # Placeholder for actual post views extraction
                            video_views = 0  # Placeholder for actual video views extraction

                            # Write the extracted data to the CSV file
                            csv_writer.writerow([account, post_views, video_views])
                    except Exception as e:
                        raise ValueError(f"Error: Failed to process file {file_path}. {str(e)}")

# Call the function to generate the CSV file
generate_csv(root_dir)
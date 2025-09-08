import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list to store the results
results = []

# Initialize the count of ads viewed
ads_viewed_count = 0

# Initialize the set of company names
company_names = set()

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON data contains the required information
            if "ads_and_topics" in data["ads_information"]:
                # Iterate over the ads and topics
                for topic in data["ads_information"]["ads_and_topics"].values():
                    # Check if the topic has a structure
                    if "structure" in topic:
                        # Iterate over the impressions history posts seen
                        for post in topic["structure"]["impressions_history_posts_seen"]:
                            # Check if the post has string map data
                            if "string_map_data" in post:
                                # Iterate over the string map data
                                for key, value in post["string_map_data"].items():
                                    # Check if the key is "Author"
                                    if key == "Author":
                                        # Increment the count of ads viewed
                                        ads_viewed_count += 1
                                        # Add the company name to the set
                                        company_names.add(value["value"])

# Create the CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    # Create the CSV writer
    writer = csv.writer(csvfile)

    # Write the column headers
    writer.writerow(["Company Name", "Number of Ads Viewed"])

    # Write the results
    for company_name in company_names:
        writer.writerow([company_name, ads_viewed_count])

# Print the results
print("Results:")
for row in csv.reader(open('query_responses/results.csv', 'r')):
    print(row)
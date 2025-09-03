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
            data = json.load(file)

            # Check if the JSON data contains the required information
            if "ads_and_topics" in data["ads_information"]:
                # Iterate over the ads and topics
                for ad, topic in data["ads_information"]["ads_and_topics"].items():
                    # Check if the ad has a type and structure
                    if "type" in topic and "structure" in topic:
                        # Check if the ad type is JSON and the structure contains impressions history ads seen
                        if topic["type"] == "json" and "impressions_history_ads_seen" in topic["structure"]:
                            # Iterate over the impressions history ads seen
                            for impression in topic["structure"]["impressions_history_ads_seen"]:
                                # Check if the impression has string map data
                                if "string_map_data" in impression:
                                    # Iterate over the string map data
                                    for key, value in impression["string_map_data"].items():
                                        # Check if the key is Author
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
print("Company Name,Number of Ads Viewed")
for company_name in company_names:
    print(f"{company_name},{ads_viewed_count}")
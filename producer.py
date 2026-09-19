from google.cloud import pubsub_v1      # pip install google-cloud-pubsub
import glob                             # for searching for json file 
import json
import os 
import csv                              # for reading CSV file
import time

# Search the current directory for the JSON file (including the service account key) 
# to set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
files = glob.glob("*.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = files[0]

# Set the project_id with your project ID
project_id = "project-f2995e59-f5d2-491f-ba8"  # Replace with your actual GCP project ID
topic_name = "csvData"        # Topic name for CSV records

# Create a publisher and get the topic path for the publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)
print(f"Publishing messages from CSV file to {topic_path}...\n")

# Path to the CSV file
csv_file_path = "Labels.csv"          # Make sure 'data.csv' exists in the directory

    # Read the CSV file and iterate over each record
with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)  # Automatically converts rows to dictionaries
    
    for row in csv_reader:
        # Convert dictionary into JSON bytes (serialization)
        record_value = json.dumps(row).encode('utf-8')
        
        try:
            # Publish the message to your topic
            future = publisher.publish(topic_path, record_value)
            
            # Ensure that publishing has been completed successfully
            future.result()
            print("The message {} has been published successfully".format(row))
        except Exception as e:
            print(f"Failed to publish the message: {e}")
        
        time.sleep(0.5)  # Wait for 0.5 second between records


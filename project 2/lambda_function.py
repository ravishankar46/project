import datetime
import requests
import mysql.connector
import time
import os
import json
import aws_lambda_logging
import logging

# Update this with your Slack webhook URL
SLACK_WEBHOOK_URL = ""

db_host = ""
db_name = ""
db_user = ""
db_password = " "

# Configure the logging module to use aws_lambda_logging
aws_lambda_logging.setup(level=logging.INFO)

def send_slack_message(message):
    payload = {
        "text": message
    }
    response = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"})
    return response.status_code == requests.codes.ok

def lambda_handler(event, context):
    while True:
        try:
            # Make a GET request to fetch the data
            response = requests.get('')

            # Get the current time
            now = datetime.datetime.now()

            # Connect to the database
            conn = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name
            )

            # Create a cursor
            cur = conn.cursor()

            # Insert the data into the database
            cur.execute("INSERT INTO iss_location (latitude, longitude, timestamp) VALUES (%s, %s, %s)", 
                        (response.json()['iss_position']['latitude'], response.json()['iss_position']['longitude'], now))

            # Commit the transaction
            conn.commit()

            # Close the database connection
            cur.close()
            conn.close()

            # Print a success message to the console
            logging.info("Data inserted successfully!")
            
        except requests.exceptions.RequestException as e:
            # Retry failed requests after 15 seconds
            logging.error(f"Request failed: {e}")
            send_slack_message('The server is unavailable!')
            time.sleep(15)
            continue

        except Exception as e:
            # Print an error message to the console if there was an issue
            logging.error(f"Error inserting data: {e}")
            time.sleep(15)
            continue

        # Wait for 15 seconds before making the next request
        time.sleep(15)

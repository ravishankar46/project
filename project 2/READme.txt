Modules:
The following Modules are used in the code:
•	datetime: used to get the current time
•	requests: used to make HTTP requests to fetch the data from the ISS API and send Slack messages
•	mysql-connector: used to connect to a MySQL database
•	time: used to add delay between requests
•	os: used to retrieve environment variables
•	json: used to create JSON payloads
•	aws_lambda_logging: used to configure logging in AWS Lambda
•	logging: used to log messages
•	Environment Variables
Environment Variables:
•	SLACK_WEBHOOK_URL: The Slack webhook URL to send messages to
•	db_host: The hostname of the MySQL database server
•	db_name: The name of the MySQL database
•	db_user: The username to authenticate to the MySQL database
•	db_password: The password to authenticate to the MySQL database
Functions:
•	send_slack_message(message): Sends a message to Slack using the specified webhook URL.
•	lambda_handler(event, context): The main function that is executed when the Lambda function is invoked.
Main Function:
lambda_handler function performs the following steps:
•	It enters a while loop that runs indefinitely.
•	It makes an HTTP GET request to the ISS API to fetch the current location data.
•	It gets the current time using the datetime.datetime.now() method.
•	It connects to the MySQL database using the credentials specified in the environment variables.
•	It creates a cursor to execute SQL queries.
•	It inserts the location data and current time into the iss_location table in the database using the cur.execute() method.
•	It commits the transaction using conn.commit().
•	It closes the cursor and database connection using cur.close() and conn.close().
•	It logs a success message to the console using logging.info().
•	If there is an exception during the execution of any of the above steps, it logs an error message to the console using logging.error(), sends a message to Slack using the send_slack_message() function, and waits for 15 seconds before continuing the loop.
Logging:
The aws_lambda_logging module is used to configure logging in the Lambda function. The level parameter in the aws_lambda_logging.setup() method is set to logging.INFO, which means that messages with a severity level of INFO and higher will be logged to the console.

Error Handling:
The code uses a try-except block to handle exceptions that may occur during the execution of the main function. If an exception occurs, it logs an error message to the console, sends a message to Slack, and waits for 15 seconds before continuing the loop. This is done to ensure that the Lambda function keeps running even if there are occasional errors in the execution of the main function.

Conclusion
Overall, the code fetches the current location of the International Space Station (ISS) from an API and inserts it into a MySQL database every 15 seconds. It also logs messages to the console and sends notifications to a Slack channel if there are any errors during the execution of the main function and says if the server was unavailable.

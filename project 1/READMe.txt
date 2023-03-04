Overview:
This script downloads a zip file containing  company facts data from the website, extracts the JSON files from the zip file,and then store them as list of dictionaries uploads the JSON files to an S3 bucket, and then populates a DynamoDB table with the data from the JSON files.
Required Libraries:
•	requests
•	zipfile
•	json
•	uuid
•	botocore
•	boto3
•	decimal
Code Explanation:
Downloading the Zip File:
•	The code first uses the requests library to download a zip file containing daily company facts data from the SEC website.
•	The headers variable contains the user-agent string to mimic a browser request.
•	The code then uses the with open() function to save the downloaded zip file.
Uploading Files to S3:
•	The script uses the boto3 library to interact with the S3 service.
•	The zipfile library is used to extract the JSON files from the downloaded zip file.
•	A list of dictionaries is created from the extracted JSON files.
•	Each dictionary is uploaded to the specified S3 bucket as a separate JSON file.
Populating DynamoDB:
•	The code uses the boto3 library to interact with the DynamoDB service.
•	A table is created or retrieved using the specified table name.
•	The JSON files are read and their data is extracted to be used in the DynamoDB items.
•	A unique UUID is generated for each item as the sort key.
•	The put_item() function is used to add the item to the DynamoDB table.
Conclusion:
This code provides a solution for downloading daily company facts data from the website, uploading the data to an S3 bucket, and populating a DynamoDB table with the data. 

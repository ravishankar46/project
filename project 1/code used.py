#This is the code i have used download the zipfile from the URL

''''
import requests
import zipfile

try:
    url = 'https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip'

    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    
    response = requests.get(url,headers = headers,stream=True)
    with open("companyfacts.zip","wb") as f:
        f.write(response.content)
        
    print("successfully downloaded the zipfile")

except Exception as e:
    print(e)
'''
#This is the code i used to extract the data and store them as list of Dictionaries adn then upload them to the s3bucket 
''''
import boto3
import zipfile
import json
import uuid
import botocore
from decimal import Decimal

# set up the S3 client with your credentials and region
session = boto3.Session(
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name=''
)
s3 = session.client('s3')

# name of the zip file to extract
zip_file_name = ""

# extract the zip file and load the data as a list of dictionaries
json_data = []
with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
    for file_name in zip_ref.namelist():
        if file_name.endswith('.json'):
            with zip_ref.open(file_name) as file:
                file_data = json.load(file, parse_float=Decimal)
                # Check if "cik" and "entityName" keys are present
                if all(key in file_data for key in ["cik", "entityName"]):
                    file_data["facts"] = file_data.get("facts", {})
                    json_data.append(file_data)
                else:
                    continue

# upload the JSON files to the existing S3 bucket
bucket_name = "guviproject1"
for data in json_data:
    file_name = data['cik']
    file_content = json.dumps(data, default=str)
    s3_key = f"{file_name}.json"
    response = s3.put_object(Bucket=bucket_name, Key=s3_key, Body=file_content)
    
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f"{file_name} uploaded successfully to S3.")
    else:
        print(f"Error uploading {file_name} to S3.")
print("successfully uploaded the files to s3")
'''
#this is the code i used to upload the data from s3 to dynamoDB
'''
# populate DynamoDB with the data from the JSON files
dynamodb = boto3.resource('dynamodb', aws_access_key_id='',
                          aws_secret_access_key='', region_name='')
table_name = ''
table = dynamodb.Table(table_name)

for data in json_data:
    if 'cik' not in data or 'entityName' not in data or 'facts' not in data:
        continue
    item = {
        'cik': data['cik'],
        'name': data['entityName'],
        'end': str(uuid.uuid4()),  # generate a unique UUID for the sort key
        'description': {},
    }
    # Split facts into smaller items if too large
    fact_items = []
    fact_size = 0
    for k, v in data['facts'].items():
        fact_size += len(k) + len(str(v))
        if fact_size > 380000:  # leave some margin for other fields
            fact_items.append(item)
            item = {
                'cik': data['cik'],
                'name': data['entityName'],
                'end': str(uuid.uuid4()),  # generate a unique UUID for the sort key
                'description': {},
            }
            fact_size = 0
        item['description'][k] = float(v) if isinstance(v, Decimal) else v
    fact_items.append(item)
    
    try:
        # Write fact items to DynamoDB
        for item in fact_items:
            response = table.put_item(Item=item)
            if 'ResponseMetadata' in response and response['ResponseMetadata']['HTTPStatusCode'] == 200:
                print(f"{item['cik']} uploaded successfully to DynamoDB.")
    except Exception as e:
        pass
print("successfully uploaded the files from s3 to dynamoDB")
'''
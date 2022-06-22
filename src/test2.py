import boto3
import os
import pandas as pd
import json
import datetime
from dotenv import load_dotenv

load_dotenv()

ID_KEY = os.getenv('ID_KEY')
SECRET_KEY = os.getenv('AWS_SECRET_KEY')

session = boto3.Session(
    aws_access_key_id=ID_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name="eu-west-3"
)
dynamodb = session.resource('dynamodb')

table = dynamodb.Table('option_data_ibex')
list_items = table.scan(AttributesToGet=['info'])['Items']
keys_list = []
for e in range(len(list_items)):
    keys = json.loads(list_items[e].get('info'))['CALL'].keys()
    for key in keys:
        keys_list.append(key)
    
dates_sorted = pd.Series(keys_list).sort_values(ascending=True).unique().tolist()
print(dates_sorted)
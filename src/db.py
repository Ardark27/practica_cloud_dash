import boto3
import os
import pandas as pd
import json

ID_KEY = os.environ.get('ID_KEY', None)
SECRET_KEY = os.environ.get('AWS_SECRET_KEY', None)
DB_TABLE = os.environ.get('DB_TABLE', None)
REGION = os.environ.get('REGION', None)

session = boto3.Session(
    aws_access_key_id=ID_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION
)
dynamodb = session.resource('dynamodb')

table = dynamodb.Table(DB_TABLE)

def get_data_from_date(date):
    response = table.get_item(
        Key={'date': date}
    )
    return json.loads(response['Item']['info'])

# json.loads(get_data_from_date(table, '2022-06-20'))[option_type].keys()

def get_all_dates():
    response = table.scan(AttributesToGet=['date'])
    data = pd.DataFrame.from_dict(response['Items']).sort_values('date').date.values.tolist()
    return data

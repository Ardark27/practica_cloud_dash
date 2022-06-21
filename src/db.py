from textwrap import indent
import boto3
from boto3.dynamodb.conditions import Key
import os
import pandas as pd
import json

# ID_KEY = os.environ.get('ID_KEY', None)
# SECRET_KEY = os.environ.get('AWS_SECRET_KEY', None)
# DB_TABLE = os.environ.get('DB_TABLE', None)

session = boto3.Session(
    aws_access_key_id='AKIA24TIIEHEDZUTAOE7',
    aws_secret_access_key='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',
    region_name='eu-west-3'
)
dynamodb = session.resource('dynamodb')

table = dynamodb.Table('option_data_ibex')

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

print(get_all_dates())
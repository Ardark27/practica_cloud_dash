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

def obtain_data_compare():
    list_items = table.scan(AttributesToGet=['info'])['Items']
    option ='CALL' 
    keys_list = []
    for e in range(len(list_items)):
        keys = json.loads(list_items[e].get('info'))[option].keys()
        # print(keys.get('2022-06-24'))
        # break
        for key in keys:
            l = len(json.loads(list_items[e].get('info'))[option][key]['strikes'])
            keys_list.append({'date': key, 'indice': e , 'count':l})    

    df = pd.DataFrame.from_dict(keys_list)
    idx = df.groupby('date')['count'].transform(max) == df['count']
    df = df[idx].drop_duplicates(subset=['date'])
    return list_items, df
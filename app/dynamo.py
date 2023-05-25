import os
import boto3
import json

def connect_to_dynamo():
    ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1', 
        aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    return dynamodb

def create_table():
    dynamodb = connect_to_dynamo()
    table = dynamodb.create_table(
        TableName='Subtitles',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],

        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

def save_subtitle(json_file: str):
    dynamodb = connect_to_dynamo()
    table = dynamodb.Table('Subtitles')
    with open(json_file) as json_file:
        data = json.load(json_file)
        for item in data:
            table.put_item(Item=item)

def upload_data(json_file: str):
    dynamodb = connect_to_dynamo()
    table = dynamodb.Table('Subtitles')
    with open(json_file) as json_file:
        data = json.load(json_file)
        for item in data:
            table.put_item(Item=item)
    
def search_data(search_phrase: str):
    dynamodb = connect_to_dynamo()
    table = dynamodb.Table('Subtitles')
    
    response = table.scan(
        FilterExpression='contains(#text, :search_phrase)',
        ExpressionAttributeNames={
            '#text': 'text'
        },
        ExpressionAttributeValues={
            ':search_phrase': search_phrase
        }
    )

    return response['Items']

def delete_table():
    dynamodb = connect_to_dynamo()
    table = dynamodb.Table('Subtitles')
    table.delete()

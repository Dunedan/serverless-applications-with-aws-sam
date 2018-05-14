import boto3
import os

client = boto3.client('dynamodb')

def handler(event, context):
    response = client.update_item(TableName=os.environ['DYNAMODB_TABLE'],
                                  Key={'id': {'S': 'counter'}},
                                  AttributeUpdates={'number': {
                                      'Action': 'ADD',
                                      'Value': {'N': '1'}}
                                  },
                                  ReturnValues='UPDATED_NEW')

    counter_value = int(response['Attributes']['number']['N'])

    return {
        "headers": {"content-type": "text/plain"},
        "body": counter_value
    }

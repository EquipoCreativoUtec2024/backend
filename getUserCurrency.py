# Retorna la cantidad de monedas de un usuario
import boto3
import json

dynamodb = boto3.client('dynamodb')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': str(err) if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
    }


def lambda_handler(event, context):
    print("Event", event)
    print("Context", context)

    operations = {
        'GET': lambda dynamo, x: dynamo.get_item(**x),
    }

    operation = event['requestContext']["http"]["method"]
    if operation in operations:

        payload = {"TableName": "users", "Key": {"username": {"S": event['queryStringParameters']['username']}}}
        retrievedItem = dynamodb.get_item(**payload)
        if "Item" not in retrievedItem:
            return ValueError('No user was found with that username')
        
        response = { 'currency' : float(retrievedItem['Item']['currency']['N'])}
        return respond(None, response)
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
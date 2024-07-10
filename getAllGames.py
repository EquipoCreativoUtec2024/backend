# Retorna la lista de juegos disponibles (en general)
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
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
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
        payload = {"TableName": "games"}
        retrievedItem = dynamodb.scan(**payload)
        
        response = retrievedItem['Items']
        
        for x in response:
            x['pretty_name'] = x['pretty_name']['S']
            x['id'] = x['id']['S']
            x['color'] = x['color']['S']
            x['route'] = x['route']['S']
        
        return respond(None, response)
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
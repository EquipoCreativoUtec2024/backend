# Activado despues de cada partida. Suma una pequeña cantidad de moneda al usuario.
import boto3
import json
from random import randint

dynamodb = boto3.client('dynamodb')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': str(err) if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,PUT'
        },
    }


def lambda_handler(event, context):
    print("Event", event)
    print("Context", context)

    bodyContent = json.loads(event['body'])

    operations = {
        'PUT': lambda dynamo, x: dynamo.put_item(**x),
    }

    operation = event['requestContext']["http"]["method"]
    if operation in operations:
        item = dynamodb.get_item(TableName = 'users', Key = {'username': {'S' : bodyContent['username']}})
        
        currency = item['Item']['currency']['N']
        
        currency = int(currency) + randint(1, 5)
        
        item['Item']['currency']['N'] = str(currency)
        
        response = dynamodb.put_item(TableName = 'users', Item = item['Item'])
        
        return(None, response)
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
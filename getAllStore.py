# Funcion para retornar todos los objetos en la tienda
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
        payload = {"TableName": "store"}
        retrievedItem = dynamodb.scan(**payload)
        
        response = retrievedItem['Items']
        
        for x in response:
            x['pretty_name'] = x['pretty_name']['S']
            x['item_name'] = x['item_name']['S']
            x['cost_in_game'] = float(x['cost_in_game']['N'])
            x['cost_real'] = float(x['cost_real']['N'])
        
        return respond(None, response)
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
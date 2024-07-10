# Crea un nuevo objeto en la tienda
import boto3
import json
from decimal import Decimal

dynamo = boto3.client('dynamodb')


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
        'POST': lambda dynamo, x: dynamo.put_item(**x),
    }

    operation = event['requestContext']["http"]["method"]
    if operation in operations:
        eventBody = json.loads(event['body'], parse_float=Decimal)
        payload = {
            "TableName": "store", 
            "Item": {
                "item_name": {
                    "S": eventBody['item_name']
                },
                "cost_in_game": {
                    "N": str(eventBody['cost_in_game'])
                },
                "cost_real" : {
                    "N": str(eventBody['cost_real'])
                }
            },
            "ConditionExpression": "attribute_not_exists(item_name)"
        }
        try: 
            createdItem = dynamo.put_item(**payload)
        except Exception as e: 
            print(str(e))
            return respond(ValueError("That name already exists."))
        
        response = createdItem
        return respond(None, response)
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
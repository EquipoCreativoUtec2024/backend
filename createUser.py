# Crea un nuevo usuario siempre que el nombre de usuario no exista en la base de datos. Si se da un usuario válido de referido, a ambos usuarios se les suma 300 monedas.
import boto3
import json
import random

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
    
    startingGames = ['faceoff', 'canas']

    operations = {
        'POST': lambda dynamo, x: dynamo.put_item(**x),
    }

    operation = event['requestContext']["http"]["method"]
    if operation in operations:
        selectedGame = random.choice(startingGames)
        eventBody = json.loads(event['body'])
        
        currency = 0
        
        if 'referal' in eventBody:
            payload = {"TableName": "users", "Key": {"username": {"S": eventBody['referal']}}}
            retrievedItem = dynamo.get_item(**payload)
            if "Item" in retrievedItem:
                currency = 300
                retrievedItem['Item']['currency']['N'] = str(float(retrievedItem['Item']['currency']['N']) + 300)
                dynamo.put_item(TableName = 'users', Item = retrievedItem['Item'])
        
        payload = {
            "TableName": "users", 
            "Item": {
                "username": {
                    "S": eventBody['username']
                },
                "currency": {
                    "N": str(currency)
                },
                "purchase_history" : {
                    "L": []
                },
                "owned_games": {
                    "SS": [selectedGame]
                },
                "password": {
                    "S": eventBody['password']
                }
            },
            "ConditionExpression": "attribute_not_exists(username)"
        }
        try: 
            createdItem = dynamo.put_item(**payload)
        except:
            return respond(ValueError("That username already exists."))
        
        response = createdItem
        return respond(None, response)
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
# Agrega el juego al usuario, resta el costo y genera un registro en el historial de compras
import boto3
import json
from datetime import date

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
        
        currency = float(currency) - float(bodyContent['price'])
        
        item['Item']['currency']['N'] = str(currency)
        
        games = item['Item']['owned_games']['SS']
        games.append(bodyContent['game_id'])
        
        item['Item']['owned_games']['SS'] = games
        
        history = {'M' : {
            'date' : {'S' : str(date.today())},
            'item_id' : {'S' : bodyContent['game_id']},
            'amount' : {'N' : str(bodyContent['price'])}
            }
        }
        item['Item']['purchase_history']['L'].append(history)
        
        response = dynamodb.put_item(TableName = 'users', Item = item['Item'])
        
        return(None, response)
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
import boto3
import json
import os

def handler(event, context):
    game_id = event.get("queryStringParameters", {}).get("game_id")
    print(f"Game ID: {game_id}")

    if not game_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Game ID is required'}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TavernGames_Dev')

    # Retrieve the game record from DynamoDB
    response = table.get_item(Key={'game_id': game_id})
    print(f"Response from DynamoDB: {response}")

    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Game not found'}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    game_record = response['Item']
    print(f"Game record: {game_record}")

    return {
        'statusCode': 200,
        'body': json.dumps(game_record),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
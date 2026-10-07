import json
import os
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME', 'Puntajes')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    juego_param = None
    if event.get('queryStringParameters'):
        juego_param = event['queryStringParameters'].get('juego')
    
    try:
        if juego_param:
            response = table.query(KeyConditionExpression=Key('juego').eq(juego_param))
            items = response.get('Items', [])
        else:
            response = table.scan()
            items = response.get('Items', [])
            
        juegos_dict = {}
        for item in items:
            j = item['juego']
            if j not in juegos_dict:
                juegos_dict[j] = []
            juegos_dict[j].append(item)
            
        resultado = {}
        for j, records in juegos_dict.items():
            records_sorted = sorted(records, key=lambda x: int(x['puntaje']), reverse=True)
            resultado[j] = records_sorted[:10]
            
        body = resultado.get(juego_param, []) if juego_param else resultado

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(body, default=str)
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}
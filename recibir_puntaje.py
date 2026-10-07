import json
import os
import boto3

sqs = boto3.client('sqs')
QUEUE_URL = os.environ.get('QUEUE_URL')

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        jugador = body.get('jugador')
        juego = body.get('juego')
        puntaje = body.get('puntaje')
        
        if not jugador or not juego or not isinstance(puntaje, int):
            return {'statusCode': 400, 'body': json.dumps({'error': 'Datos invalidos o puntaje no es entero'})}
        
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps({'jugador': str(jugador), 'juego': str(juego), 'puntaje': puntaje})
        )
        
        return {
            'statusCode': 202, 
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': 'Puntaje encolado'})
        }
    except Exception:
        return {'statusCode': 400, 'body': json.dumps({'error': 'JSON invalido'})}
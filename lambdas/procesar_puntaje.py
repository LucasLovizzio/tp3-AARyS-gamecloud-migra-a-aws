import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME', 'Puntajes')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    for record in event.get('Records', []):
        try:
            body = json.loads(record['body'])
            jugador = body['jugador']
            juego = body['juego']
            nuevo_puntaje = int(body['puntaje'])
            
            response = table.get_item(Key={'juego': juego, 'jugador': jugador})
            item = response.get('Item')
            
            if not item or nuevo_puntaje > int(item['puntaje']):
                table.put_item(Item={'juego': juego, 'jugador': jugador, 'puntaje': nuevo_puntaje})
                print(f"Puntaje guardado: {jugador} en {juego} -> {nuevo_puntaje}")
            else:
                print(f"El puntaje {nuevo_puntaje} no supera al actual para {jugador}")
        except Exception as e:
            print(f"Error: {str(e)}")
            raise e
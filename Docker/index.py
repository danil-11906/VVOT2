from PIL import Image
import requests
from io import BytesIO
import boto3
import json
import os
import ydb
from sanic import Sanic
from sanic.response import text
import sanic.response as response

app = Sanic(__name__)


@app.after_server_start
async def after_server_start(app, loop):
    print(f"App listening at port {os.environ['PORT']}")


@app.route("", methods=['GET', 'POST'])
async def hello(request):
    bucket = 'itis-2022-2023-vvot39-photos'
    new_bucket = 'itis-2022-2023-vvot39-faces'
    ip = request.headers["X-Forwarded-For"]

    json_msg = json.loads(request.json['messages'][0]['details']['message']['body'])
    photo = json_msg['object_id']


    x1 = int(json_msg['vertices'][0]['x'])
    y1 = int(json_msg['vertices'][0]['y'])
    x2 = int(json_msg['vertices'][2]['x'])
    y2 = int(json_msg['vertices'][2]['y'])

    url = 'https://storage.yandexcloud.net/' + bucket + '/' + photo
    r = requests.get(url)
    im = Image.open(BytesIO(r.content))
    im.crop((x1, y1, x2, y2)).save(photo, quality=95)
    session = boto3.session.Session(region_name='ru-central1')
    s3 = session.client(
        aws_access_key_id='', #TODO get key-id
        aws_secret_access_key='', #TODO get secret-key
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        region_name='ru-central1'
    )
    face = str(request.json['messages'][0]['details']['message']['message_id']) + str(photo)
    s3.upload_file(photo, new_bucket, face)

    ydb_client = session.client('dynamodb', endpoint_url='https://docapi.serverless.yandexcloud.net/ru-central1/b1g71e95h51okii30p25/etnig856uuujqnekk95m', aws_access_key_id='', aws_secret_access_key='') #TODO key_id, secret-key

    table = ydb_client.create_table(
      TableName='task2',
      KeySchema=[
          {
          'AttributeName': 'id',
           'KeyType': 'HASH'
          }
      ],
      AttributeDefinitions=[
          {
          'AttributeName': 'id',
          'AttributeType': 'S'
          },
          {
          'AttributeName': 'photo',
          'AttributeType': 'S'
          },
          {
          'AttributeName': 'face',
          'AttributeType': 'S'
          },
          {
          'AttributeName': 'name',
          'AttributeType': 'S'
          }
          ]
      )

    ydb_client.put_item(TableName='task2', Item={
        'id': {
            'S': str(request.json['messages'][0]['details']['message']['message_id']) },
        'name': { 
                 'S': ''},
        'photo': {
            'S': photo},
        'face': {
            'S': face}
                                 })


    return response.json(
        {'message': "Handled."},
        status=200
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ['PORT']), motd=False, access_log=False)

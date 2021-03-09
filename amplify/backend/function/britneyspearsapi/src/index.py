import awsgi
import os
from uuid import uuid4
from flask import Flask, jsonify, request
from flask_cors import CORS

import boto3

app = Flask(__name__)
CORS(app)

client = boto3.client('dynamodb')

BASE_ROUTE = "/song"

TABLE = os.environ.get("STORAGE_BRITNEYSONGS_NAME")

@app.route(BASE_ROUTE + '/<song_id>', methods=['GET'])
def get_song(song_id):
    song = client.get_item(TableName=TABLE, Key={
        'id': {
            'S': song_id
        }
    })
    return jsonify(data=song)


@app.route(BASE_ROUTE + '/<song_id>', methods=['DELETE'])
def delete_song(song_id):
    client.delete_item(
        TableName=TABLE,
        Key={'id': {'S': song_id}}
    )
    return jsonify(message="song deleted")


@app.route(BASE_ROUTE + '/', methods=['POST'])
def create_song():
    request_json = request.get_json()
    client.put_item(TableName=TABLE, Item={
        'id': { 'S': str(uuid4()) },
        'name': {'S': request_json.get("name")},
        'year': {'S': request_json.get("year")},
        'link': {'S': request_json.get("link")},
    })
    return jsonify(message="song created")


@app.route(BASE_ROUTE + '/<song_id>', methods=['PUT'])
def update_song(song_id):
    # Change to your fields
    client.update_item(
        TableName=TABLE,
        Key={'id': {'S': song_id}},
        UpdateExpression='SET #name = :name, #year = :year, #link = :link',
        ExpressionAttributeNames={
            '#name': 'name',
            '#year': 'year',
            '#link': 'link'
        },
        ExpressionAttributeValues={
            ':name': {'S': request.json['song_name']},
            ':year': {'S': request.json['year']},
            ':link': {'S': request.json['link']},
        }
    )
    return jsonify(message="item updated")


@app.route(BASE_ROUTE + '/', methods=['GET'])
def list_songs():
    return jsonify(data=client.scan(TableName=TABLE))


def handler(event, context):
    return awsgi.response(app, event, context)

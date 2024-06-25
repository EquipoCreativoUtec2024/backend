from dataclasses import dataclass
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route('/', methods=['GET'])
def route_index():
    return jsonify({'message': 'Hello, World!'})

if __name__ == '__main__':
    app.run(host="0.0.0.0")
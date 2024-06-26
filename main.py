#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, desc
from flask_cors import CORS

app = Flask(__name__)

cache = {}

CORS(app, origins='*')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@dataclass
class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    dislikes = db.Column(db.Integer, nullable=False)
    ratio = db.Column(db.Float, nullable=False)
    tag = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()
    
@app.route('/questions', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def route_questions():
    if request.method == 'GET':
        questions = Questions.query.order_by(Questions.ratio.desc()).all()
        question_list = [{'id': question.id, 'question': question.question, 'author' : question.author, 'likes': question.likes, 'dislikes': question.dislikes, 'ratio': question.ratio, 'type' : question.tag} for question in questions]
        
        if len(question_list) < 100:
            question_list = question_list[:len(question_list) - 1]
        else :
            question_list = question_list[:99]
            
        if 'questions' in cache:
            return cache['questions']
        else:
            cache['questions'] = jsonify(question_list)
        return jsonify(question_list)
    
    elif request.method == 'POST':
        question_data = request.get_json()
        new_question = Questions(question = question_data['question'], author = question_data['author'], likes = 0, dislikes = 0, ratio = 0)
        db.session.add(new_question)
        db.session.commit()
        del cache['questions']
        return 'SUCCESS'
    elif request.method == 'PUT':
        question_data = request.get_json()
        question = Questions.query.get(question_data['id'])
        if question_data['action'] == 'like':
            question.likes += 1
        elif question_data['action'] == 'dislike':
            question.dislikes += 1
        question.ratio = question.likes / (question.likes + question.dislikes)
        db.session.commit()
        del cache['questions']
        return 'SUCCESS'
    elif request.method == 'DELETE':
        question_data = request.get_json()
        question = Questions.query.get(question_data['id'])
        db.session.delete(question)
        db.session.commit()
        del cache['questions']
        return 'SUCCESS'

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
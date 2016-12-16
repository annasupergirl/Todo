import pymongo, json

from flask import Flask, render_template, jsonify, request, abort
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util

app = Flask(__name__)
mongo = MongoClient()

db = mongo.todo_database

@app.route('/')
def index():
    return render_template("start.html")

@app.route('/todo',methods=['GET'])
def getTaskList():
    try:
        tasks = db.todo_list.find()

        return json_util.dumps(tasks)
    except Exception,e:
        return jsonify(status='ERROR',message=str(e))

@app.route('/todo/<string:task_id>',methods=['GET'])
def getTask(task_id):
    try:
        task = db.todo_list.find_one({'_id':ObjectId(task_id)})

        if task:
            return json_util.dumps(task)
        else:
            abort(404)

    except Exception,e:
        return jsonify(status='ERROR',message=str(e))

@app.route('/todo',methods=['POST'])
def addTask():
    try:
        json_data = json.loads(request.data) 
        title = json_data['task']
        done = json_data['done']

        db.todo_list.insert_one({ 'title': title, 'done': done })
        return jsonify(status='OK',message='inserted successfully')

    except Exception,e:
        return jsonify(status='ERROR',message=str(e))

@app.route('/todo/<string:task_id>',methods=['PATCH'])
def updateTask(task_id):
    try:
        taskInfo = json.loads(request.data)
        title = taskInfo['task']
        done = taskInfo['done']

        db.todo_list.update_one({'_id':ObjectId(task_id)},{'$set':{'title':title, 'done':done}})
        return jsonify(status='OK',message='updated successfully')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))

@app.route('/todo/<string:task_id>',methods=['DELETE'])
def deleteTask(task_id):
    try:
        db.todo_list.delete_one({'_id':ObjectId(task_id)})
        return jsonify(status='OK',message='deletion successful')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))

if __name__ == "__main__":
    app.run()

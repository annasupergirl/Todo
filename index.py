import pymongo, json

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
mongo = MongoClient()

db = mongo.test_database

@app.route('/')
def index():
    return render_template("start.html")

@app.route('/todo',methods=['POST'])
def addTask():
    try:
    	json_data = json.loads(request.data)
        task = json_data['task']
        done = json_data['done']

        # title, selected: false
        db.testing.insert_one({ 'task': task, 'done': done })
        return jsonify(status='OK',message='inserted successfully')

    except Exception,e:
        return jsonify(status='ERROR',message=str(e))

@app.route('/todo',methods=['GET'])
def getTaskList():
    try:
        tasks = db.testing.find()
        
        taskList = []
        for task in tasks:
            taskItem = {
                'id': str(task['_id']),
                'task': task['task'],
                'done': task['done']
            }
            taskList.append(taskItem)

    except Exception,e:
        return str(e)
    return json.dumps(taskList)

@app.route('/todo<string:task_id>',methods=['GET'])
def getTask():
    try:
        tasks = db.testing.find({'_id':ObjectId(task_id)})
        
        for task in tasks:
            taskItem = {
                'id': str(task['_id']),
                'title': task['task'],
                'done': task['done']
            }

        print taskItem

    except Exception,e:
        return str(e)
    return json.dumps(taskItem)

@app.route('/todo/<string:task_id>',methods=['PUT'])
def updateTask(task_id):
    try:
        taskInfo = json.loads(request.data)
        task = taskInfo['task']
        done = taskInfo['done']

        db.testing.update_one({'_id':ObjectId(task_id)},{'$set':{'task':task, 'done':done}})
        return jsonify(status='OK',message='updated successfully')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))

@app.route('/todo/<string:task_id>',methods=['DELETE'])
def deleteTask(task_id):
    try:
        db.testing.delete_one({'_id':ObjectId(task_id)})
        return jsonify(status='OK',message='deletion successful')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))

if __name__ == "__main__":
    app.run()

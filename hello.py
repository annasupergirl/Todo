import pymongo

from flask import Flask
# from flask.ext.pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)
# mongo = PyMongo(app)

connection = MongoClient()

db = connection.test_database

result = db.test.insert_one({'x': 1})

# db.users.insert_one( { 'name':'user 1', 'level':1 } )
# db.users.insert_one( { 'name':'user 2', 'level':2 } )
# db.users.insert_one( { 'name':'user 3', 'level':3 } )

print result.inserted_id

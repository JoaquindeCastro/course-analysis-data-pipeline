import os
import pymongo

pwd = os.environ.get('MONGO_USER_PWD')
db = 'esca'

def client():
	return pymongo.MongoClient(f"mongodb+srv://Joaquin:{pwd}@cluster0.uchry.mongodb.net/{db}?retryWrites=true&w=majority")
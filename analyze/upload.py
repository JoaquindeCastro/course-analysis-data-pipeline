import json

def fileToDB(file, db):
	data = []

	with open(file,'r') as f:
		for line in f:
			data.append(json.loads(line))

	db.courses.insert_many(data)
import pymongo
import time

client = pymongo.MongoClient("localhost:27017")
db = client.esca

sorted_price = db.courses.find().sort("price",-1)
sp = {}
for i,course in enumerate(sorted_price):
	sp[course['_id']] = i+1

most_enrolled = db.courses.aggregate([
	{"$sort":{"enrolled":-1}},
	{"$limit":10}
])

for course in most_enrolled:
	print(course['enrolled'],course['name'],"on",course['platform'], course['price'],course['duration'],course['rating'],sp[course['_id']])

print(time.perf_counter())
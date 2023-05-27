import matplotlib.pyplot as plt
import pymongo

client = pymongo.MongoClient("localhost:27017")
courses = client.esca.courses

X = [course['price'] for course in courses.find()]
Y = [course['enrolled'] for course in courses.find()]

def plot(x,y):
	X = [course[x] for course in courses.find()]
	Y = [course[y] for course in courses.find()]
	plt.plot(X,Y,'o')
	plt.show()
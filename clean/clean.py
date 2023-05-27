import os
import json

os.chdir("..")
base_dir = os.getcwd()
in_file = os.path.join(base_dir,"ingest","courses.jsonl")
out_file = os.path.join(base_dir,"clean","courses.jsonl")

master_links = []

def appendData(data,out):
	d = {}
	with open(out,'a') as f:
		if data['source'] not in master_links:
			master_links.append(data['source'])
			f.write("\n")
			d['name'] = data['name']
			d['provider'] = data['provider']
			d['price'] = cleanPrice(data)
			d['duration'] = float(data['duration'])
			d['tags'] = getTags(data)
			d['softwares'] = getSoftwares(data)
			d['rating'] = scaleRating(data)
			d['number_of_ratings'] = data['number_of_ratings']
			d['enrolled'] = data['enrolled']
			d['platform'] = data['platform']
			d['source'] = data['source']
			f.write(json.dumps(d))

def filter(data):
	""" Filter based on number of enrollees and language """
	if "enrolled" not in data:
		return False
	if data["enrolled"] == 0:
		return False
	if "language" in data and data["language"] != "English":
		return False
	return True

def isLinkedIn(data):
	""" Checks if course is on the LinkedIn Learning platform"""
	if data["platform"] == "LinkedIn":
		return True
	return False

def cleanPrice(data):
	""" Cleans price and convert to a float """
	price = data['price']
	try:
		return float(price)
	except:
		price = str(price)
		price = price.replace("PHP","") \
		.replace("$","") \
		.replace("USD","") \
		.replace(",","")
		return float(price)

def getTags(data):
	""" Returns tags for a course based on course name """
	keywords = {
		"architectural":['architectural','architecture','architect'],
		"electrical":['electrical','electric','mep'],
		"mechanical":['mechanical','mechanics','mep'],
		"plumbing":['plumbing','mep'],
		"structural":['structural','structure'],
		"detailing":['detailing'],
		"families":['families','family'],
		"parametric families":['parametric families','parametric family'],
		"API":['api'],
		"transportation":["roads","highways","transportation","transport"],
		"management":["manager","management","manage"],
		"VDC":['vdc']

	}
	tags = []
	name = data['name'].lower()
	for tag, keywords in keywords.items():
		if any(keyword in name for keyword in keywords):
			tags.append(tag)
	return tags

def getSoftwares(data):
	""" Returns BIM softwares for a course based on course name """
	softwares = []
	software_list = [
		"Revit","AutoCAD","BIM 360","Revizto",
		"Navisworks","ArchiCAD","Vectorworks Architect","Edificius",
		"Midas Gen","Solibri","Dynamo","IES-VE","InfraWorks"
		]
	name = data['name'].lower()
	for software in software_list:
		if software.lower() in name:
			softwares.append(software)
	return softwares


def scaleRating(data):
	""" Scales 1.0-5.0 rating to 0.0-1.0"""
	rating = data['rating']
	return rating/5

""" Filters and adjusts LinkedIn course details """
with open(in_file,'r') as f:
	for course in f:
		course = json.loads(course)
		if 	filter(course) == True:
			if isLinkedIn(course) == True:
				course['number_of_ratings'] = course['likes']
				course['rating'] = 4.0 # each like is equivalent to a rating of 4
			appendData(course,out_file)
			
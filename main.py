from db_connect import client
from analyze.upload import fileToDB

client = client()
db = client.esca

if __name__ == '__main__':
	fileToDB('clean/courses.jsonl',db)
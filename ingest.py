import requests
from bs4 import BeautifulSoup as bsp
import pandas
import pymongo

client = pymongo.MongoClient("localhost:27017")
db = client.esca


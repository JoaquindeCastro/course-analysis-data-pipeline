''' Web scraper for Udemy.com '''
import time
import re
import requests
import json
from os import path
import colorama
from termcolor import colored

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException,InvalidArgumentException

''' GET EXCHANGE RATE FOR USD TO PHP '''
r = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
rates = r.json()['rates']
convert = float(rates['PHP'])

""" Configurate driver options """
options = webdriver.ChromeOptions()
options.add_argument("start-maximized");
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

driver = webdriver.Chrome(options=options)
driver.get('https://www.udemy.com/course/teklastructures/')

duration = 0
container = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,'main-content-wrapper')))
name = container.find_element_by_class_name('clp-lead__title--small').text
description = container.find_element_by_class_name('clp-lead__headline').text
enrolled = container.find_element_by_css_selector('div[data-purpose=enrollment]').text
enrolled = int(enrolled.replace(',','').split(' ')[0])
language = container.find_element_by_class_name('clp-lead__locale').text
provider = container.find_element_by_class_name('udlite-instructor-links')
provider = provider.find_element_by_tag_name('span').text
purchase_container = driver.find_element_by_css_selector('div[data-purpose=purchase-section]')
try:
	price = WebDriverWait(purchase_container,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div[data-purpose=course-old-price-text]')))
	price = price.find_element_by_css_selector('span s span').get_attribute('innerHTML')
except:
	price = purchase_container.find_element_by_css_selector('div[data-purpose=course-price-text]')
	price = price.find_element_by_css_selector('span span').get_attribute('innerHTML')
price = str(price).replace('$','').replace(',','')
price = float(price)*convert
rating = container.find_element_by_css_selector('span[data-purpose=rating-number]').text
rating = float(rating)
rating_string = container.find_element_by_css_selector('div[data-purpose=rating]').text
if "ratings)" in rating_string:
	number_of_ratings = re.search("\((.*?)ratings\)",rating_string).group(1) # If number of ratings is in the form (n ratings)
else:
	number_of_ratings = re.search("\((.*?)\)",rating_string).group(1)
number_of_ratings = int(''.join(i for i in number_of_ratings if i.isdigit())) # If number of ratings is in the form (n)

""" Write data to JSON Lines file """
new = {
	"name":name,
	"provider":provider,
	"price":float(price),
	"type":["online"],
	"tags":[],
	"duration":duration,
	"enrolled":enrolled,
	"rating":rating,
	"number_of_ratings":number_of_ratings,
	"language":language,
	"platform":"Udemy",
	"source":link,
}
""" Web scraper for LinkedIn Learning website
"""

import time
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

colorama.init()

USERNAME = 'Joaquin'
CHROME_PROFILE = 'Profile 1'
PATH = f"C:\\Users\\{USERNAME}\\AppData\\Local\\Google\\Chrome\\User Data\\{CHROME_PROFILE}"

QUERY = 'BIM'
URL = f'https://www.linkedin.com/learning/search?entityType=COURSE&keywords={QUERY}'

def scroll_down(driver):
	""" Scroll to bottom of dynamically loading web page """

	last_height = driver.execute_script("return document.body.scrollHeight") # Get scroll height.

	while True:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll down
		time.sleep(3) # Wait to load rest of page
		new_height = driver.execute_script("return document.body.scrollHeight") # Check if new content was loaded
		if new_height == last_height:
			break
		last_height = new_height

""" Get exchange rate from USD to PHP """
r = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
rates = r.json()['rates']
convert = float(rates['PHP'])

""" Configurate driver options """
options = webdriver.ChromeOptions()
options.add_argument("start-maximized");
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

if not path.exists(PATH):
	print(colored('Chrome profile PATH not found, please check the USERNAME and CHROME_PROFILE or specify a different path.','red'))
	exit()
try:
	options.add_argument(f"user-data-dir={PATH}")
except InvalidArgumentException:
	print(colored('This Chrome profile is already in use, please close other windows.','red'))
	exit()
except:
	print(colored('Error with Chrome profile','red'))

""" Get and load entire page """
driver = webdriver.Chrome(options=options)
driver.get(URL)

scroll_down(driver)

""" Scrape Courses """
time.sleep(2)
courses = driver.find_elements_by_class_name('entity-link')

links = {a.get_attribute('href') for a in courses}
print(links)

data = []

for link in links:

	driver.get(link)
	time.sleep(2)
	try:
		enroll_button = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,'upsell-button'))) # Also serves as buffer for page to fully load.

		name = driver.find_element_by_class_name('course-overview-header__entity-link').text
		if 'revit' not in name.lower():
			raise Exception
		meta_data = driver.find_element_by_class_name('course-overview-meta-list')
		duration = meta_data.find_element_by_css_selector('li:nth-child(2)').text
		duration = duration.split('h')[0]
		enrolled = driver.find_element_by_class_name('lls-card-viewer-count').text
		enrolled = int(enrolled.split(" ")[0].replace(",",""))
		instructor = driver.find_element_by_class_name('course-overview-author-cards__card-content').text
		try:
			likes = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[contains(text(), "members like")]'))).text
			likes = int(likes.split(" ")[0].replace(",",""))
		except:
			likes = 0
		enroll_button.click() # Go to check out page to get price
		time.sleep(2)

		if "login" in str(driver.current_url):
			""" Check if driver is redirected to login page 

			This assumes that at least one signed in profile exists, and clicks the first one 
			in order to proceed to check out page.
			"""
			try:
				driver.find_element_by_class_name('member-profile-block').click()
			except:
				print(colored('Log In Error: A signed in LinkedIn profile could not be found.','red'))
				driver.execute_script("alert('Log In Error: This Chrome profile is not logged in to Coursera, please log in.');")
				exit()

		price = driver.find_element_by_class_name('lil-content__cart-info--price').text

		new = {
			"name":name,
			"provider":instructor,
			"price":price,
			"type":["online"],
			"tags":[],
			"duration":duration,
			"enrolled":enrolled,
			"likes":likes,
			"platform":'LinkedIn',
			"source":link,
		}
		with open('courses.jsonl','a') as f:
			f.write("\n")
			f.write(json.dumps(new))
	except:
		continue

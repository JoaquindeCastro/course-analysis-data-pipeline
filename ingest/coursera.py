""" Web scraper for Coursera website
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


driver = webdriver.Chrome(options=options)
driver.get('https://www.coursera.com')


""" Check if Chrome Profile is logged in """
try:
	WebDriverWait(driver,3).until(EC.presence_of_element_located((By.LINK_TEXT,"Log In")))
	print(colored('Log In Error: This Chrome profile is not logged in to Coursera, please log in.','red'))
	try:
	    driver.execute_script("alert('Log In Error: This Chrome profile is not logged in to Coursera, please log in.');")
	    time.sleep(1)
	    driver.quit()
	except WebDriverException:
	    pass
	exit()
except:
	print(colored('This Chrome profile is logged in, executing script...','green'))


"""Search for 'Revit'"""
search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "react-autosuggest__input")))
time.sleep(1)
search.send_keys('Revit')
time.sleep(1)
search.send_keys(Keys.RETURN)

""" Filter for only English courses """
time.sleep(3)
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div[data-e2e=allLanguages]"))).click()
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"input[value=English]"))).click()


""" Scrape Courses """
next_button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"button[data-e2e=pagination-controls-next]")))

while True:

	""" Scrape individual page by courses """

	next_button = WebDriverWait(driver,10).until(EC.presence_of_element_located(
		(By.CSS_SELECTOR,"button[data-e2e=pagination-controls-next]")))
	courses = driver.find_elements_by_class_name('rc-DesktopSearchCard')

	for course in courses:
		course.click()
		driver.switch_to.window(driver.window_handles[-1])

		try:
			container = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.TAG_NAME,'main')))
			name = container.find_element_by_class_name('banner-title').text
			instructor = container.find_element_by_css_selector('a[data-track-component=nav_item_instructors]')
			instructor = instructor.find_element_by_tag_name('span').text
			enrolled = container.find_element_by_class_name('rc-ProductMetrics')
			enrolled = container.find_element_by_css_selector('span strong span').text
			enrolled = int(enrolled.replace(',',''))
			rating_container = container.find_element_by_class_name('XDPRating')
			rating = rating_container.find_element_by_class_name('number-rating').text
			rating = float(rating.replace('\nstars',''))
			number_of_ratings = rating_container.find_element_by_class_name('_wmgtrl9')
			number_of_ratings = number_of_ratings.find_element_by_tag_name('span').text
			number_of_ratings = int(number_of_ratings.split(" ")[0].replace(",",""))
			about_section = container.find_element_by_class_name('AboutCourse')
			duration = about_section.find_element_by_xpath('//span[contains(text(), "hours")]').get_attribute('innerHTML')
			duration = int(''.join(i for i in str(duration) if i.isdigit()))

			WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'button[data-e2e=enroll-button]'))).click()
			price = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//span[contains(text(), "$")]'))).text
			price = float(price.replace("PHP","").replace("$","").replace(",",""))*convert

			new = {
				"name":name,
				"provider":instructor,
				"price":price,
				"type":["online"],
				"tags":[],
				"duration":int(duration),
				"enrolled":enrolled,
				"rating":rating,
				"number_of_ratings":number_of_ratings,
				"platform":"Coursera",
				"source":str(driver.current_url),
			}
			with open('courses.jsonl','a') as f:
				f.write("\n")
				f.write(json.dumps(new))

		except:
			print("failed")


		driver.close()
		driver.switch_to.window(driver.window_handles[0])

	if "arrow-disabled" in next_button.get_attribute('class'):
		break
	else:
		next_button.click()

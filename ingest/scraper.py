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

class Coursera:

	def __init__(self,driver):
		self.driver = driver

	def is_logged_in(self):
		if True:
			return True
		return False

	def filter(self,query=None,language=None):
		if query is not None:
			WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "react-autosuggest__input")))
			.send_keys('Revit')
			.send_keys(Keys.RETURN)

		if language is not None:
			time.sleep(2)
			WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div[data-e2e=allLanguages]"))).click()
			WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"input[value=English]"))).click()

		def get_next_button(self):


	def scrape(self):
		""" Scrape Courses """
		next_button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"button[data-e2e=pagination-controls-next]")))

		while "arrow-disabled" not in next_button.get_attribute('class'):

			""" Scrape individual page by courses """

			courses = driver.find_elements_by_class_name('rc-DesktopSearchCard')

			for course in courses:
				course.click()
				driver.switch_to.window(driver.window_handles[-1])

				try:
					container = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.TAG_NAME,'main')))
					name = container.find_element_by_class_name('banner-title').text
					if 'revit' not in name.lower():
						raise Exception
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

			next_button.click()
			next_button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"button[data-e2e=pagination-controls-next]")))
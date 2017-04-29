from selenium import webdriver
import os

# browser = webdriver.Chrome('C:/Users/adam/Desktop/chromedriver.exe')
#                            C:\Users\adam\Desktop/geckodriver.exe
# browser = webdriver.Firefox('c:/Users/adam/Desktop/firefox/geckodriver.exe')
browser = webdriver.Chrome('c:/Users/adam/Desktop/chromedriver.exe')
browser.get('http://localhost:8000')

assert 'Django' in browser.title

# so this doesn't work at all
# browser.Dispose()

# doesn't work either
# browser.Quit()

# trying it the windows way
# doesn't run the test before killing itself, huh...
# of course this only works if there's no assertion error
# os.system('taskkill /im chrome.exe /f')


# from selenium import webdriver

# browser = webdriver.Firefox()

# FROM THE WEBPAGE
# 
# Edith has heard about a cool new online to-do app. She goes
# to check out its homepage
# browser.get('http://localhost:8000')

# She notices the page title and header mention to-do lists
assert 'To-Do' in browser.title

# She is invited to enter a to-do item straight away

# She types "Buy peacock feathers" into a text box (Edith's hobby
# is tying fly-fishing lures)

# When she hits enter, the page updates, and now the page lists
# "1: Buy peacock feathers" as an item in a to-do list

# There is still a text box inviting her to add another item. She
# enters "Use peacock feathers to make a fly" (Edith is very methodical)

# The page updates again, and now shows both items on her list

# Edith wonders whether the site will remember her list. Then she sees
# that the site has generated a unique URL for her -- there is some
# explanatory text to that effect.

# She visits that URL - her to-do list is still there.

# Satisfied, she goes back to sleep

browser.quit()
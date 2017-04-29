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
os.system('taskkill /im chrome.exe /f')

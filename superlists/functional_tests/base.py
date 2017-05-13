import os
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
from selenium import webdriver

# to run a single test file:
# python manage.py test functional_tests.test_list_item_validation

MAX_WAIT = 10

# you have to inherit from LiveServerTestCase
class FunctionalTest(StaticLiveServerTestCase):

    # remember, only methods that begin with test_ will get run as tests, so
    # you can use other methods for your own purposes  
    # 
    # Do you remember I said
    # that LiveServerTestCase had certain limitations? Well, one is that it
    # always assumes you want to use its own test server, which it makes
    # available at self.live_server_url.
    def setUp(self):
        self.browser = webdriver.Chrome('C:/Users/adam/Desktop/chromedriver.exe')
        # staging server by default uses djangos dev server
        # this changes that so that it looks for an environmental variable 
        staging_server = os.environ.get('STAGING_SERVER') 
        if staging_server:
            self.live_server_url = 'http://' + staging_server  

    # will execute even if there is an error
    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    # def check_for_row_in_list_table(self, row_text):
    #     table = self.browser.find_element_by_id('id_list_table')
    #     rows = table.find_elements_by_tag_name('tr')
    #     self.assertIn(row_text, [row.text for row in rows])


    # helper method to check todo list contents
    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:  
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return  
            except (AssertionError, WebDriverException) as e:  
                if time.time() - start_time > MAX_WAIT:  
                    raise e  
                time.sleep(0.5)  

    # helper method that ensures that a function runs before selenium
    # looks for items on the page
    # expects to be passed a function
    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                # calls the function that was passed to it
                # returns its response
                return fn()  
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

from .server_tools import reset_database

# to run a single test file:
# python manage.py test functional_tests.test_list_item_validation


MAX_WAIT = 10
print('base called')

# you have to inherit from LiveServerTestCase
class FunctionalTest(StaticLiveServerTestCase):

    # helper method for getting it_text
    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    # remember, only methods that begin with test_ will get run as tests, so
    # you can use other methods for your own purposes
    #
    # Do you remember I said
    # that LiveServerTestCase had certain limitations? Well, one is that it
    # always assumes you want to use its own test server, which it makes
    # available at self.live_server_url.
    # def setUp(self):
    #     self.browser = webdriver.Chrome('C:/selenium-driver/chromedriver.exe')
    #     # staging server by default uses djangos dev server
    #     # this changes that so that it looks for an environmental variable
    #     staging_server = os.environ.get('STAGING_SERVER')
    #     print(staging_server, 'WHAT THE ACTUAL FUCK')
    #     if staging_server:
    #         print('ooo can do')
    #         self.live_server_url = 'http://' + self.staging_server


    def setUp(self):
        self.browser = webdriver.Chrome('C:/selenium-driver/chromedriver_32.exe')
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            self.live_server_url = 'http://' + self.staging_server
            reset_database(self.staging_server)


    # will execute even if there is an error
    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()


    def wait(fn):
        def modified_fn(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return fn(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > MAX_WAIT:
                        raise e
                    time.sleep(0.5)
        return modified_fn


    # def check_for_row_in_list_table(self, row_text):
    #     table = self.browser.find_element_by_id('id_list_table')
    #     rows = table.find_elements_by_tag_name('tr')
    #     self.assertIn(row_text, [row.text for row in rows])


    # helper method to check todo list contents
    # def wait_for_row_in_list_table(self, row_text):
    #     start_time = time.time()
    #     while True:
    #         try:
    #             table = self.browser.find_element_by_id('id_list_table')
    #             rows = table.find_elements_by_tag_name('tr')
    #             self.assertIn(row_text, [row.text for row in rows])
    #             return
    #         except (AssertionError, WebDriverException) as e:
    #             if time.time() - start_time > MAX_WAIT:
    #                 raise e
    #             time.sleep(0.5)



    # helper method that ensures that a function runs before selenium
    # looks for items on the page
    # expects to be passed a function

    # This has been replaced here with a decorator function but it's still used
    # in: test_login.py
    # def wait_for(self, fn):
    #     start_time = time.time()
    #     while True:
    #         try:
    #             # calls the function that was passed to it
    #             # returns its response
    #             return fn()
    #         except (AssertionError, WebDriverException) as e:
    #             if time.time() - start_time > MAX_WAIT:
    #                 raise e
    #             time.sleep(0.5)

    # Does the same as above but uses the decorator.
    @wait
    def wait_for(self, fn):
        return fn()

    # def wait_to_be_logged_in(self, email):
    #     self.wait_for(
    #         lambda: self.browser.find_element_by_link_text('Log out')
    #     )
    #     navbar = self.browser.find_element_by_css_selector('.navbar')
    #     self.assertIn(email, navbar.text)


    # def wait_to_be_logged_out(self, email):
    #     self.wait_for(
    #         lambda: self.browser.find_element_by_name('email')
    #     )
    #     navbar = self.browser.find_element_by_css_selector('.navbar')
    #     self.assertNotIn(email, navbar.text)





    @wait
    def wait_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])


    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element_by_link_text('Log out')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)


    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)

    def add_list_item(self, item_text):

        print('I AM THE LIZARD QUEEN')
        num_rows = len(self.browser.find_elements_by_css_selector('#id_list_table tr'))
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        item_number = num_rows + 1
        self.wait_for_row_in_list_table(f'{item_number}: {item_text}')
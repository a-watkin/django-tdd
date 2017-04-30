from django.core.urlresolvers import resolve
from django.test import TestCase
from lists.views import home_page
from django.http import HttpRequest

from django.template.loader import render_to_string

from lists import views


# Create your tests here.
class SmokeTest(TestCase):

    def test_root_url_resolves_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        # home_page is a method of lists views
        # so it sends the request to home_page
        response = home_page(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        expected_html = render_to_string('home.html')
        self.assertEqual(html, expected_html)

    # this test is a simpler version of the one directly above
    # and can also replace test_root_url_resolves_to_home_page
    def test_home_page_returns_correct_html(self):
        # instead of creating a request object this is a shortcut
        # you just pass it the url you want
        response = self.client.get('/')  

        html = response.content.decode('utf8')  
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))

        # checks the correct templates was used
        # ONY WORKS FOR RESPONSES RETRIEVED BY THE TEST CLIENT
        # so self.client.get()
        self.assertTemplateUsed(response, 'home.html') 

        # deliberately breaking the test to ensure it works
        # self.assertTemplateUsed(response, 'wrong.html')

# this is the refactored version of the class above 
class HomePageTest(TestCase):
    # don't test constants like html strings, test implementation
    # the above literal tests are examples
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
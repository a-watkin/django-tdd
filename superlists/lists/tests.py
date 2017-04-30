from django.core.urlresolvers import resolve
from django.test import TestCase
from lists.views import home_page
from django.http import HttpRequest

from django.template.loader import render_to_string

# for the database tests
from lists.models import Item

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

    def test_can_save_post_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()


        # Django also gives us an API for querying the database via a class
        # attribute, .objects, and we use the simplest possible query, .all(),
        # which retrieves all the records for that table. The results are
        # returned as a list-like object called a QuerySet, from which we can
        # extract individual objects, and also call further functions, like
        # .count().
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')
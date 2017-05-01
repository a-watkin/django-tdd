from django.core.urlresolvers import resolve
from django.test import TestCase
from lists.views import home_page

# for the database tests
from lists.models import Item


# this is the refactored version of the class above 
class HomePageTest(TestCase):
    # don't test constants like html strings, test implementation
    # the above literal tests are examples
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    # always redirect after a POST
    def test_can_save_a_POST_request(self):
        self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')


    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


    def test_displays_all_list_items(self):
        # sets up the test
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')
        # calls code under test
        response = self.client.get('/')
        # checks
        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())

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


    
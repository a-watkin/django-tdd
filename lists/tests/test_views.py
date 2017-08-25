from django.test import TestCase
from django.utils.html import escape

from lists.forms import (
    DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR,
    ExistingListItemForm, ItemForm,
)
from lists.models import Item, List

# this is the refactored version of the class above 
class HomePageTest(TestCase):
    # don't test constants like html strings, test implementation
    # the above literal tests are examples
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{}/'.format(list_.id))
        self.assertTemplateUsed(response, 'list.html')


    # Here’s a new helper method: instead of using the slightly annoying
    # assertIn/response.content.decode() dance, Django provides the
    # assertContains method which knows how to deal with responses and the
    # bytes of their content.
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/lists/{}/'.format(correct_list.id))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/{}/'.format(correct_list.id))
        self.assertEqual(response.context['list'], correct_list)  


    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(
            f'/lists/{list_.id}/',
            data={'item_text': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_displays_item_form(self):
        # creates a new list_ object
        list_ = List.objects.create()
        # gets the url to that object created above
        response = self.client.get(f'/lists/{list_.id}/')
        # asserts that the request has a form object, 
        # form is just one of many context?
        # 
        # ItemForm is the name of the class in forms.py
        # context is just for testing, its the django built in faux browser
        self.assertIsInstance(response.context['form'], ItemForm)
        # response has the name in the context above? as text
        # 
        self.assertContains(response, 'name="text"')

    # helper method
    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            f'/lists/{list_.id}/',
            data={'text': ''}
        )

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    # @skip
    # def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
    #     list1 = List.objects.create()
    #     item1 = Item.objects.create(list=list1, text='textey')
    #     response = self.client.post(
    #         f'/lists/{list1.id}/',
    #         data={'text': 'textey'}
    #     )

    #     expected_error = escape(DUPLICATE_ITEM_ERROR)
    #     # expected_error = escape("You've already got this in your list")
    #     # checks the expected error is the same as the constant
    #     self.assertContains(response, expected_error)
    #     # checks that list.html is returned
    #     self.assertTemplateUsed(response, 'list.html')
    #     # checks the number of items in the list is 1
    #     self.assertEqual(Item.objects.all().count(), 1)


    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')
        response = self.client.post(
            f'/lists/{list1.id}/',
            data={'text': 'textey'}
        )

        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'text': 'A new list item'})
        # tests if the item is saved to the database
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


    # this fucking thing
    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')


    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)


    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        # so it has to be this? yup this breaks it
        response = self.client.post(
            f'/lists/{correct_list.id}/',
            # should be text and not item_text
            data={'text': 'A new item for an existing list'}
        )
        self.assertRedirects(response, '/lists/{}/'.format(correct_list.id))

    # replaced by methods below
    # def test_validation_errors_are_sent_back_to_home_page_template(self):
    #     response = self.client.post('/lists/new', data={'item_text': ''})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'home.html')

    #     # escape because there's an ' in the string and django html escapes those
    #     expected_error = escape("You can't have an empty list item")
    #     # print(response.content.decode())
    #     self.assertContains(response, expected_error)


    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


    # If there’s a validation error, we should render the home template, with
    # a 200.
    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    # If there’s a validation error, the response should contain our error
    # text.
    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    # If there’s a validation error, we should pass our form object to the
    # template.
    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)


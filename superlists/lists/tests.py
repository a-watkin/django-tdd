from django.core.urlresolvers import resolve
from django.test import TestCase
from lists.views import home_page

# for the database tests
from lists.models import Item, List


# this is the refactored version of the class above 
class HomePageTest(TestCase):
    # don't test constants like html strings, test implementation
    # the above literal tests are examples
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)


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

        # compares list objects, behind the scenes they're tested with their ids
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)


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


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        # tests if the item is saved to the database
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
        # 
        # the above two asserts can be replaced with:
        # 
        
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/{}/'.format(new_list.id))


    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/{}/add_item'.format(correct_list.id),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/{}/add_item'.format(correct_list.id),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, '/lists/{}/'.format(correct_list.id))
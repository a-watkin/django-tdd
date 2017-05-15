from django.test import TestCase
from lists.models import Item, List
from unittest import skip
from django.core.exceptions import ValidationError

class ListAndItemModelsTest(TestCase):

    # if you don't give a comment for a skip it skips but counts as a pass
    # if you give a comment it will show as a skip ..S... in the output
    # @skip('because')
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




    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        
        # tests if the assertion is raised
        # this wraps around the item.save()
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
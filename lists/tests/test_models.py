from django.test import TestCase
from lists.models import Item, List
from unittest import skip
from django.core.exceptions import ValidationError

# class ListAndItemModelsTest(TestCase):

    # if you don't give a comment for a skip it skips but counts as a pass
    # if you give a comment it will show as a skip ..S... in the output
    # @skip('because')
    # def test_saving_and_retrieving_items(self):
    #     list_ = List()
    #     list_.save()

    #     first_item = Item()
    #     first_item.text = 'The first (ever) list item'
    #     first_item.list = list_
    #     first_item.save()

    #     second_item = Item()
    #     second_item.text = 'Item the second'
    #     second_item.list = list_
    #     second_item.save()

    #     saved_list = List.objects.first()
    #     self.assertEqual(saved_list, list_)


    #     # Django also gives us an API for querying the database via a class
    #     # attribute, .objects, and we use the simplest possible query, .all(),
    #     # which retrieves all the records for that table. The results are
    #     # returned as a list-like object called a QuerySet, from which we can
    #     # extract individual objects, and also call further functions, like
    #     # .count().
    #     saved_items = Item.objects.all()
    #     self.assertEqual(saved_items.count(), 2)

    #     first_saved_item = saved_items[0]
    #     second_saved_item = saved_items[1]
    #     self.assertEqual(first_saved_item.text, 'The first (ever) list item')

    #     # compares list objects, behind the scenes they're tested with their ids
    #     self.assertEqual(first_saved_item.list, list_)
    #     self.assertEqual(second_saved_item.text, 'Item the second')
    #     self.assertEqual(second_saved_item.list, list_)


class ItemModelTest(TestCase):
    # above replaced with the following two methods
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())



class ListModelTest(TestCase):

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')

        # tests if the assertion is raised
        # this wraps around the item.save()
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

    # test duplicate list items raise an integrity error
    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()
            # will cause an error if you don't use full_clean
            # item.save()

    # tests that two separate lists can have the same item
    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()  # should not raise


    # test ordering of database items, apparently
    # Items.objects.all() can get out of step with the database
    # with some uniqueness constraints 
    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='3')
        # this does cause an assertionError but it's not very human readable 
        self.assertEqual(
            # Django querysets don’t compare well with lists.
            # 
            # so you need to convert the queryset to a list
            # Item.objects.all(),
            # [item1, item2, item3]

            # convert the query set to a list:
            list(Item.objects.all()),
            [item1, item2, item3]
        )



    # tests human readable representations of database items
    def test_string_representation(self):
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')
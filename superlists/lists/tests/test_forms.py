from django.test import TestCase
# imports the error message constant and the form
from lists.forms import EMPTY_ITEM_ERROR, ItemForm


class ItemFormTest(TestCase):

    # def test_form_renders_item_text_input(self):
    #     form = ItemForm()
    #     # form.as_p() renders the form as HTML
    #     # 
    #     # so self.fail just fails no matter what?
    #     self.fail(form.as_p())


    def test_form_item_input_has_placeholder_and_css_classes(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())


    # inputs data into the form, here it's a blank string which causes it to
    # fail, because it can't validate form data that's blank as defined in the
    # view (full.clean, forces the model to validate the data isn't blank)
    # 
    # 
    # The API for checking form validation before we try and save any data is
    # a function called is_valid
    # this also adds the error message that is wanted
    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        # uses constant from forms.py
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])
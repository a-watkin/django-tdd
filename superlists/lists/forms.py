# first example
# from django import forms

# class ItemForm(forms.Form):
#     item_text = forms.CharField(
#         widget=forms.fields.TextInput(attrs={
#             'placeholder': 'Enter a to-do item',
#             'class': 'form-control input-lg',
#         }),
#     )



from django import forms
from lists.models import Item

# constant for form error
EMPTY_ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this in your list"

# In Meta we specify which model the form is for, and which fields we want it
# to use.

class ItemForm(forms.models.ModelForm):

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg',
            }),
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }

    # needed so the form can save to the database
    def save(self, for_list):
        # The .instance attribute on a form represents the database object
        # that is being modified or created.
        self.instance.list = for_list
        # directly uses the model class
        return super().save()


class ExistingListItemForm(ItemForm):
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        # takes the error message adjusts it and passes it back into the form
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)
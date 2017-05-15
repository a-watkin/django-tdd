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
from django.shortcuts import redirect, render
from lists.models import Item, List
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.utils.html import escape

# Create your views here.
# def home_page(request):
    # if request.method == 'POST':
        # new_item_text = request.POST['item_text']
        # this also saves to the database
        # Item.objects.create(text=new_item_text)

    # else:
        # holds post contents of an empty string
        # new_item_text = ''

    # if request.method == 'POST':
    #     return HttpResponse(request.POST['item_text'])
    # return render(request, 'home.html', {
        # dict method get()
        # Return the value for key if key is in the dictionary, else
        # default. If default is not given, it defaults to None, so that
        # this method never raises a KeyError.
        # 'new_item_text': request.POST.get('item_text', ''),
        # })

    # the above return statement refactored
    # return render(request, 'home.html', {
    #     'new_item_text': new_item_text
    #     })


def home_page(request):
    return render(request, 'home.html')

def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        # deletes the empty item so the test passes
        list_.delete()
        error = "You can't have an empty list item"

        return render(request, 'home.html', {"error": error})

    # return redirect('/lists/{}/'.format(list_.id))
    # 
    # does the same as above but using reverse lookup
    # it's defined in the models module, get_absolute_url
    return redirect(list_)

# list_id is captured from the url.py capture group (.+)
def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            # so if the method is post create an item object with the supplied
            # text, then return that item list url
            item = Item(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            # absolute url
            return redirect(list_)

        except ValidationError:
            error = "You can't have an empty list item"

    # passes the items to the page as items
    # 
    # you must pass the error too
    return render(request, 'list.html', {'list': list_, 'error': error})

# replaced with the view above
# 
# def add_item(request, list_id):
#     # gets a reference to the list_id object passed in the url
#     list_ = List.objects.get(id=list_id)
#     # adds the post data to the list_ object
#     Item.objects.create(text=request.POST['item_text'], list=list_)
#     # redirects to the page of that list
#     return redirect('/lists/{}/'.format( list_.id ) )


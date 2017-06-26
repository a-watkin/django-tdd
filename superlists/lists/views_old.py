from django.shortcuts import redirect, render
from lists.models import Item, List
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.utils.html import escape
from lists.forms import ItemForm
from lists.models import Item, List

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
    return render(request, 'home.html', {'form': ItemForm()})

# uses form data
def new_list(request):
    # passes the request.POST data into the form’s constructor.
    form = ItemForm(data=request.POST)
    # form.is_valid() to determine whether this is a good or a bad submission.
    if form.is_valid():
        list_ = List.objects.create()
        # print('getting here')
        form.save(for_list=list_)
        return redirect(list_)
    # if form data is bad return the template, which will handle
    # displaying an error message
    else:
        return render(request, 'home.html', {"form": form})

    # return redirect('/lists/{}/'.format(list_.id))
    # 
    # does the same as above but using reverse lookup
    # it's defined in the models module, get_absolute_url
    return redirect(list_)

# list_id is captured from the url.py capture group (.+)

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=list_)
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})
    # return render(request, 'list.html', {'list': list_, "form": form})

# replaced with the view above
# 
# def add_item(request, list_id):
#     # gets a reference to the list_id object passed in the url
#     list_ = List.objects.get(id=list_id)
#     # adds the post data to the list_ object
#     Item.objects.create(text=request.POST['item_text'], list=list_)
#     # redirects to the page of that list
#     return redirect('/lists/{}/'.format( list_.id ) )

from django.shortcuts import redirect, render
from lists.models import Item


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
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/the-only-list-in-the-world/')

def view_list(request):
    # gets all the items from the database
    items = Item.objects.all()
    # passes the items to the page as items
    return render(request, 'list.html', {'items': items})
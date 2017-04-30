from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home_page(request):
    # if request.method == 'POST':
    #     return HttpResponse(request.POST['item_text'])
    return render(request, 'home.html', {
        # dict method get()
        # Return the value for key if key is in the dictionary, else
        # default. If default is not given, it defaults to None, so that
        # this method never raises a KeyError.
        'new_item_text': request.POST.get('item_text', ''),
        })
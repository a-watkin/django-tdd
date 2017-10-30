"""superlists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from lists import views as list_views
from lists import urls as list_urls
from accounts import urls as accounts_urls


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', list_views.home_page, name='home'),
    # url(r'^lists/new$', views.new_list, name='new_list'),


    # It’s time to learn how we can pass parameters from URLs to views: (.+)
    # is a capture group, it matches any character up to the /  
    # 
    # In other
    # words, if we go to the URL /lists/1/, view_list will get a second
    # argument after the normal request argument, namely the string "1". If we
    # go to /lists/foo/, we get view_list(request, "foo").
    # url(r'^lists/(\d+)/$', views.view_list, name='view_list'),

    # url(r'^lists/(\d+)/add_item$', views.add_item, name='add_item'),


    # url(r'^$', list_views.home_page, name='home'),
    url(r'^lists/', include(list_urls)),

    # url(r'accounts/', include(account_urls)),

    url(r'^accounts/', include(accounts_urls)),


    url(r'^about/', list_views.about_page, name='about'),

]

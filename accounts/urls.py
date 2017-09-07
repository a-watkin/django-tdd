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
from django.conf.urls import url
from accounts import views
from django.contrib.auth.views import logout

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'^$', views.home_page, name='home'),
    # 
    # django prefixes these with /list...remember?
    # url(r'^new$', views.new_list, name='new_list'),


    # It’s time to learn how we can pass parameters from URLs to views: (.+)
    # is a capture group, it matches any character up to the /  
    # 
    # In other
    # words, if we go to the URL /lists/1/, view_list will get a second
    # argument after the normal request argument, namely the string "1". If we
    # go to /lists/foo/, we get view_list(request, "foo").
    # url(r'^/', views.send_login_email, name='home_redirect'),

    # url(r'^(\d+)/add_item$', views.add_item, name='add_item'),



    # name='send_login_email' was missing here.
    url(r'^send_login_email', views.send_login_email, name='send_login_email'),

    # url(r'^login$', views.redirect_after_login, name='login'),

    url(r'^login$', views.login, name='login'),

]
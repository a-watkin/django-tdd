from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from accounts.models import Token
from django.core.urlresolvers import reverse


def send_login_email(request):
    email = request.POST['email']
    print('this thing',type(send_mail))
    token = Token.objects.create(email=email)
    # builds a URI, the is apparently the best way to do itfmd  #.request
    url = request.build_absolute_uri(  
        reverse('login') + '?token=' + str(token.uid)
    )
    print(url)
    send_mail(
        'Your login link for Superlists',
        'Use this link to log in {}'.format(url),
        'noreply@superlists',
        [email]
    )

    messages.success(
    request,
    "Check your email, we've sent you a link you can use to log in."
    )
    return redirect('/')


def redirect_after_login(request):
    print('redirect_after_login called')
    param1 = request.get_raw_uri()
    print(param1)
    return redirect('/')

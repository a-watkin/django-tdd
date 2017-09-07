import uuid
from django.contrib import auth
from django.db import models


# Decouples this file form django signals, signals notify components about
# events, here it causes a problem because there's no last_login field 
auth.signals.user_logged_in.disconnect(auth.models.update_last_login)


class User(models.Model):
    # email = models.EmailField(unique=True)
    email = models.EmailField(primary_key=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True


class Token(models.Model):
    email = models.EmailField()
    uid = models.CharField(default=uuid.uuid4, max_length=40)

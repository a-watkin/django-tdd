from django.db import models

# Create your models here.
class Item(models.Model):
    # a new field means a new migration
    text = models.TextField(default='')


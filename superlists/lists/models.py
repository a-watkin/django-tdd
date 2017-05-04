from django.db import models


class List(models.Model):
    pass

    
# Create your models here.
class Item(models.Model):
    # a new field means a new migration
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)



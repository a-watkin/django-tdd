from django.db import models
from django.core.urlresolvers import reverse


class List(models.Model):
    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])


class Item(models.Model):
    # unique=True here would mean that it would have to be unique across
    # all todo lists
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)

    def __str__(self):
        return self.text

    # specify that a list item should be unique within a list
    class Meta:
        
        # 
        # specify ordering
        ordering = ('id',)

        # Sets of field names that, taken together, must be unique
        # 
        # one to many only
        unique_together = ('list', 'text')



from django.db import models
#from .tags.models import Tag

# Create your models here.
class Note(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    #tags = models.ManyToManyField(Tag)
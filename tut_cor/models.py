from django.db import models
from django.db.models.fields import CharField, DateField, PositiveSmallIntegerField, TextField


# Create your models here.
class Content(models.Model):
    title=CharField(max_length=30)
    subject=CharField(max_length=40)
    description=TextField()
    Links=TextField()
    date_created=DateField(auto_now_add=True, null=True)
    rate=PositiveSmallIntegerField(default=0)
    rated=TextField(default='p')
    author=CharField(max_length=50)

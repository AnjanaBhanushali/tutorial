from django.db import models
from datetime import datetime
from django.db.models.fields import DateTimeField

# Create your models here.
class employees(models.Model):
    """
    fname=models.CharField(max_length=10,null=True)
    lname=models.CharField(max_length=10,null=True)
    emp_id=models.IntegerField(null=True)
    """
    msg_id=models.CharField(max_length=100,null=True)
    isImportant=models.BooleanField(default=False)
    picture=models.ImageField(default='default.png',blank=True)
    form = models.TextField(null=True)
    subject = models.TextField(null=True)
    message = models.TextField(null=True)
    timestamp = models.DateTimeField(default=datetime.now,null=False)
    isRead = models.BooleanField(default=False)



    def __str__(self):
        return self.msg_id
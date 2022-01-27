from django.db import models
from jsonfield import JSONField
from django.utils import timezone

class ProductDetails(models.Model):
    """Declaring the Products Model"""
    sku = models.CharField(max_length=2000, blank=False, default='')
    title = models.CharField(max_length=70000, blank=False, default='')
    price = models.CharField(max_length=200,blank=False, default='' )
    description = models.CharField(max_length=70000, blank=False, default='')
    ratings = models.JSONField(default = dict())
    timestamp = models.DateTimeField(auto_now_add=True) #Values entered in db current time
    

class HtmlModel(models.Model):
    """Declaring the HTML model"""
    sku = models.CharField(max_length=10000, blank=False, default='')
    _html = models.TextField(max_length=70000, blank=False, default='')

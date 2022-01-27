from django.contrib import admin
from .models import ProductDetails,HtmlModel


class ProductDetailsAdmin(admin.ModelAdmin):
    fields= [
        'sku',
        'title',
        'price',
        'description',
        'ratings',                
        'timestamp',
        ]
    
    readonly_fields= []

    class Meta:
        model= ProductDetails

# Register your models here.
admin.site.register(ProductDetails)

admin.site.register(HtmlModel)
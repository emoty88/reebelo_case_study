from django.contrib import admin
from products.models import *

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderProduct)


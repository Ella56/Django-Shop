from django.contrib import admin

from .models import Status,Cart,OrderItems

# Register your models here.

admin.site.register(Status)
admin.site.register(Cart)
admin.site.register(OrderItems)

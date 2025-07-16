from django.contrib import admin
from .models import Category,Tag,Blog,Blog_Comment,Blog_Reply
# Register your models here.


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Blog)
admin.site.register(Blog_Comment)
admin.site.register(Blog_Reply)
from django.contrib import admin
from .models import Profile,Province,City,Address,User

# Register your models here.


admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Province)
admin.site.register(City)
admin.site.register(Address)
from django.contrib import admin
from .models import User, UserPermission, Permission

admin.site.register(User)
admin.site.register(UserPermission)
admin.site.register(Permission)

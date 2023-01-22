from django.contrib import admin
from .models import User
from todoapp.models import Project, Todo

# Register your models here.

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Todo)

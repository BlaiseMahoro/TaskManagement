from django.contrib import admin
from .models import Profile, Project, Role

admin.site.register(Project)
admin.site.register(Profile)
admin.site.register(Role)

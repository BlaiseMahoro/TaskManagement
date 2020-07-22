from django.contrib import admin
from .models import Profile, Project, Role, Comment, Ticket, TicketTemplate, File, Attribute, Type, State, AttributeType
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']

admin.site.register(Project)
admin.site.register(Profile)
admin.site.register(Role)
admin.site.register(TicketTemplate)
admin.site.register(Ticket)
admin.site.register(File)
admin.site.register(Comment)
admin.site.register(Attribute)
admin.site.register(State)
admin.site.register(Type)
admin.site.register(AttributeType)

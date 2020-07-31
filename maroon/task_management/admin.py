from django.contrib import admin
from .models import Profile, Project, Role, Comment, Ticket, TicketTemplate, File, Attribute, Type, State, AttributeType
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']

class AttributeInlineAdmin(admin.TabularInline):
    model = Attribute
    extra = 0
class TicketAdmin(admin.ModelAdmin):
    inlines = [AttributeInlineAdmin]

class StateInlineAdmin(admin.TabularInline):
    model = State
    extra = 0
class TypeInlineAdmin(admin.TabularInline):
    model = Type
    extra = 0
class AttributeTypeInlineAdmin(admin.TabularInline):
    model = AttributeType
    extra = 0


class TicketTemplateAdmin(admin.ModelAdmin):
    inlines = [StateInlineAdmin, TypeInlineAdmin, AttributeTypeInlineAdmin]
    list_display=('project',)


admin.site.register(Project)
admin.site.register(Profile)
admin.site.register(Role)
admin.site.register(TicketTemplate, TicketTemplateAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(File)
admin.site.register(Comment)
admin.site.register(Attribute)
admin.site.register(State)
admin.site.register(Type)
admin.site.register(AttributeType)

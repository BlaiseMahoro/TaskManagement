from django.contrib import admin
from .models import Profile, Project, Role, Comment, Ticket, TicketTemplate, File, Attribute, Type, State, AttributeType, ProjectAdmin, TicketAdmin
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']

class AttributeInlineAdmin(admin.TabularInline):
    model = Attribute
    extra = 0
class CommentInlineAdmin(admin.TabularInline):
    model = Comment
    extra = 0
class TicketAdmin(admin.ModelAdmin):
    inlines = [AttributeInlineAdmin,CommentInlineAdmin]

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

class RoleInlineAdmin(admin.TabularInline):
    model = Role
    extra = 0

class ProjectAdmin(admin.ModelAdmin):
    inlines = [RoleInlineAdmin]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Profile)
#admin.site.register(Role)
admin.site.register(TicketTemplate, TicketTemplateAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(File)
#admin.site.register(Comment)
#admin.site.register(Attribute)
#admin.site.register(State)
#admin.site.register(Type)
#admin.site.register(AttributeType)
